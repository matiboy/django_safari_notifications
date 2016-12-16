from django.core.management.base import BaseCommand
from django.apps import apps
import os, sys, shutil
from django_safari_notifications.views import ICON_SIZES

config = apps.get_app_config('django_safari_notifications')
logger = config.logger

# Checks to see if user has installed Pillow
try:
    from PIL import Image
except ImportError:
    logger.error('Pillow is required to use this command. Install Pillow and try again')
    # Error code in sys.exit - ends the process
    sys.exit(1)

class Command(BaseCommand):
    help = 'Creates the set of icons (iconset) required for the Safari Push Package'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('original_file_path', type=str, help='The absolute path to icon file for resizing')

        # Named (optional) arguments
        parser.add_argument(
            '-o',
            '--output',
            dest='destination',
            default=os.getcwd(),
            help='Specify the absolute path for output directory of icons'
        )
        parser.add_argument(
            '--no-create',
            action='store_true',
            dest='no_create',
            default=False,
            help='Does not create a directory for iconset'
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            dest='overwrite',
            default=False,
            help='Overwrites directory or files if exist'
        )

    def handle(self, *args, **options):
        input_file_path = options['original_file_path']
        output_folder_path = options['destination'] + '/'

        # If overwrite is true, will delete files and directory in output path/current directory
        if options['overwrite']:
            # Checks to see if directory exists and sets delete path
            dir_exists = os.path.isdir(os.path.join(options['destination'], 'icon.iconset/'))
            if dir_exists:
                delete_path = './icon.iconset/'
            else:
                delete_path = './'

            for size in ICON_SIZES:
                try:
                    os.remove('{}icon_{}.png'.format(delete_path, size))
                except FileNotFoundError:
                    pass

            if dir_exists:
                try:
                    os.rmdir('./icon.iconset')
                except OSError:
                    logger.error('Could not remove directory: ', OSError)

        # Creates a directory for iconset based on whether no_create flag is true/false
        if not options['no_create']:
            output_folder_path = os.path.join(options['destination'], 'icon.iconset/')
            # Try catch to make directory - catches if file not found, folder already exists, folder not writable
            try:
                os.mkdir(output_folder_path)
            except (FileExistsError, FileNotFoundError, OSError) as e:
                logger.error(e)
                return

        # Try catch to open image file and assigns to an instance of the Image class
        try:
            im = Image.open(input_file_path)
        except IOError as e:
            logger.error('Invalid image, could not open: ', e)
            return

        # For values in ICON_SIZES, copies an image, creates thumbnails - based on whether normal or @2x and saves to output
        for size in ICON_SIZES:
            copy = im.copy()
            thumbnail_size = int(size.split('x')[0])
            try:
                if size.endswith('x'):
                    # Makes pixels xratio
                    ratio = int(size[-2:-1])
                    thumbnail_tuple = (thumbnail_size * ratio, thumbnail_size * ratio)
                else:
                    # Makes pixels x1
                    thumbnail_tuple = (thumbnail_size, thumbnail_size)
                # Creates thumbnail
                copy.thumbnail(thumbnail_tuple, Image.LANCZOS)
            except IOError as e:
                logger.error('Error creating thumbnail for image: ', e)

            # Saves image to destination
            try:
                copy.save('{}icon_{}.png'.format(output_folder_path, size))
            except (IOError, FileExistsError) as e:
                logger.error('Error saving image: ', e)
                return

        logger.info(self.style.SUCCESS('Successfully made iconsets at {}'.format(output_folder_path)))
