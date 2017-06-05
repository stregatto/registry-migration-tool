
from k8s_tool import K8s_tool
from docker_tool import Docker_tool
from log_file import Log_file
import argparse


class Registry_tool(object):


    def __init__(self):
        self.k8s = K8s_tool()
        self.logfile = Log_file()
        self.docker = Docker_tool()
        self.images = self.k8s.get_images_from_all_deployment()


    def migrate_registry(self, destination_registry, dryrun):
        for image in self.images:
            if not self.logfile.is_image_done(image):
                if self.docker.pull_image(image, dryrun):
                    # to do:
                    # tag image and push
                    image_name = self.docker.image_name(image)
                    new_image = '%s/%s:%s' % (destination_registry,
                                              image_name.get('repository'),
                                              image_name.get('tag'))
                    self.docker.push_image(new_image, dryrun)
                    self.docker.delete_image(image, dryrun)
                    self.logfile.image_done(image)
        return


class Interactive(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='Migrate registry, read images from kube cluster and push images into new registry')
        parser.add_argument('-r', '--remote',
                            help='remote registry (E.G. myregistry.com:5000)',
                            required=True)
        parser.add_argument('-d', '--dryrun',
                            action="count",
                            default=0,
                            required=False,
                            help='run program without pulling, pushing and deleting images')
        self.args = parser.parse_args()

    def get_args(self):
        return self.args


class Main(object):

    def __init__(self, args):
        registry = Registry_tool()
        registry.migrate_registry(args.remote, args.dryrun)

if __name__ == '__main__':
    # to do, set some switch
    print('Starting migration...')
    interactive = Interactive()
    args = interactive.get_args()
    main = Main(args)
