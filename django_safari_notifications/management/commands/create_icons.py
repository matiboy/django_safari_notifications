from django.core.management.base import BaseCommand
from django.apps import apps
import os, sys
from django_safari_notifications.views import ICON_SIZES

config = apps.get_app_config('django_safari_notifications')
# connects to logger in settings.py of connected project
logger = config.logger

# try catch to see if user has pillow installed
try:
    from PIL import Image
except ImportError:
    logger.error('Pillow is required to use this command - pip install Pillow')
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

    def handle(self, *args, **options):
        input_file_path = options['original_file_path']
        output_folder_path = options['destination'] + '/'

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
            thumbnail_arr = size.split('x')
            thumbnail_size = (int(thumbnail_arr[0]), int(thumbnail_arr[0]))

            # Try catch to create thumbnail
l            try:
                if size.endswith('x'):
                    copy.resize(thumbnail_size, Image.LANCZOS)
                else:
                    copy.thumbnail(thumbnail_size)
            except IOError as e:
                logger.error('Error creating thumbnail for image: ', e)

            # Try catch to save image to destination
            try:
                copy.save((output_folder_path + 'icon_{0}.png').format(size))
            except (IOError, FileExistsError) as e:
                logger.error('Error saving image: ', e)
                return

        logger.info(self.style.SUCCESS('Successfully made iconsets at {}'.format(output_folder_path)))
