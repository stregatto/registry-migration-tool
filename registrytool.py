
from k8stool import K8sTool
from dockertool import DockerTool
from logfile import LogFile
import argparse


class Registry_tool(object):


    def __init__(self):
        self.k8s = K8sTool()
        self.logfile = LogFile()
        self.docker = DockerTool()
        self.images = self.k8s.get_images_from_all_deployment()


    def migrate_registry(self, destination_registry, dryrun):
        for image in self.images:
            if not self.logfile.is_image_done(image):
                self.docker.pull_image(image, dryrun)
                image_name = self.docker.image_name(image)
                image_id = self.docker.get_image_id(image)
                tag = image_name.get('tag')
                image_new = '%s%s' % (destination_registry,
                                      image_name.get('repository'))
                self.docker.tag_image(image_id=image_id, repository=image_new, tag=tag)
                self.docker.push_image(image_new + ':' + tag, dryrun)
                self.docker.delete_image(image_new + ':' + tag, dryrun)
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
