import os
import errno
import sys
import argparse
import csv
import glob
from shutil import copy


DEFAULT_TEMPLATE = "./content/templates/template_producto._md"
DEFAULT_EXPORT_DIR = "./export"
DEFAULT_MD_EXTENSION = "md"
CONTENT_DIR = "content"
IMAGES_DIR = "static/images"
COLUMN_PRODUCT = "Producto"
COLUMN_CATEGORY = 'Categoria'
COLUMN_CODE = 'Codigo'
COLUMN_IMAGE_NAME = 'Nombre Imagen'
COLUMN_DESTACADO = 'Destacado'
CATEGORY_DESTACADOS = 'destacados'


def generate_and_export_files(csv_file, photo_directory, template_file, export_dir):
    reader = csv.DictReader(csv_file, delimiter=',')
    template = template_file.read()
    for row in reader:
        if row[COLUMN_PRODUCT] and row[COLUMN_CATEGORY] and row[COLUMN_CODE]:
            generate_md_and_images(row, photo_directory, template, export_dir)


def generate_md_and_images(row, photo_directory, template, export_dir):
    for column, value in row.items():
        template = replace_value(template, column, value)

    template = template.replace("{{fecha}}", "")
    images = copy_images(row, photo_directory, export_dir)
    template = replace_value(
        template, "images", generate_images_section(images))

    template = replace_value(template, "categories",
                             generate_categories_section(row))

    export_file = generate_file_name(
        "{}/{}".format(export_dir, CONTENT_DIR), row, DEFAULT_MD_EXTENSION)
    write_file(export_file, template)


def replace_value(template, var, value):
    return template.replace("{{" + var.lower() + "}}", value)


def row_value(row, column):
    value = row[column]
    return (value.lower() if value else value)


def generate_file_name(dir, row, extension, wildcard=''):
    return "{}/{}/{}{}.{}".format(dir, generate_relative_dir(row), row_value(row, COLUMN_CODE), wildcard, extension)


def generate_relative_dir(row):
    return "{}/{}".format(row_value(
        row, COLUMN_PRODUCT), row_value(row, COLUMN_CATEGORY))


def generate_images_section(images):
    formatted_images = []
    for image in images:
        image = image.replace("/static", "")
        formatted_images.append('  - image: "{}"'.format(image))

    return "\n".join(formatted_images)


def generate_categories_section(row):
    categories = []
    if row_value(row, COLUMN_DESTACADO) and row_value(row, COLUMN_DESTACADO).lower() == "si":
        categories.append(CATEGORY_DESTACADOS)
    return ",".join(categories)


def write_file(filename, content):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(content)


def copy_images(row, photo_directory, export_dir):
    target_images = []
    src_images = generate_file_name(photo_directory, row, "*", '*')
    src_files = glob.glob(src_images)
    src_files.sort()
    target_dir = "{}/{}/{}".format(export_dir,
                               IMAGES_DIR, generate_relative_dir(row))
    os.makedirs(target_dir, exist_ok=True)
    for file in src_files:
        copy(file, target_dir)
        target_images.append(target_dir + "/" + os.path.basename(file))

    return target_images


class rw_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                "{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.W_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                "{0} is not a readable nor writable dir".format(prospective_dir))


def _get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'catalog_csv', help="Catalogo del cual importar los productos", type=argparse.FileType('r'))
    parser.add_argument(
        'photo_directory', help="Directorio del cual importar las fotos de los productos", action=rw_dir)
    parser.add_argument('-e', '--export_directory', default=DEFAULT_EXPORT_DIR,
                        help="Directorio en el cual exportar los .md e imagenes", action=rw_dir)
    parser.add_argument('-t', '--template', default=DEFAULT_TEMPLATE,
                        help="Template para generar archivo md", type=argparse.FileType('r'))
    return parser.parse_args()


def main():
    args = _get_arguments()
    generate_and_export_files(
        args.catalog_csv, args.photo_directory, args.template, args.export_directory)


if __name__ == "__main__":
    main()
