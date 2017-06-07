import docker
import re
import json
import os
import sys

# TO DO, for now is not working
# now it work using:
# ocker login -u="application+servicetool" -p="M0FXZY8JF6P8QPRKBA9DSAP8YY6FDSK432Q83Q7AU52Y" registry.my-rprivate-registry:30080
class Registry(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.auth = json.loads('{ "user": "%s", "password": "%s"}' % (self.user,
                                                                      self.password))
        if not user:
            self.auth_present = False
        else:
            self.auth_present = True


class DockerTool(object):
    '''
    More or less a wrapper for docker library.
    Here I would like to add some glue to simplify the work
    '''

    def __init__(self):
        self.client = docker.APIClient(base_url='unix://var/run/docker.sock')

        self.source_registry = Registry(os.environ.get('DT_SOURCE_REGISTRY_USER', None),
                                        os.environ.get('DT_SOURCE_REGISTRY_PASSWORD', None))
        self.destination_registry = Registry(os.environ.get('DT_DESTINATION_REGISTRY_USER', None),
                                             os.environ.get('DT_DESTINATION_REGISTRY_PASSWORD', None))


    def __steamerror__(self, line):
        if 'errorDetail' in line:
            j = json.loads(line)
            raise Exception(j.get('errorDetail'))


    def __primitive_push_image__(self, image, destination_registry):
        '''
        This is a primitive to push image
        '''
        if self.destination_registry.auth_present:
            return self.client.push(image,
                                    auth_config=destination_registry.auth,
                                    stream=True,)
        else:
            return self.client.push(image,
                                    stream=True,)


    def __print_dot__(self):
        sys.stdout.write('.')
        sys.stdout.flush()


    def pull_image(self, image, dryrun=None):
        print('pulling image: %s' % image)
        if dryrun is None or dryrun is 0:
            for line in self.client.pull(image, stream=True):
                self.__print_dot__()
                self.__steamerror__(line)
        else:
            print('pull_image -- dryrun: %s' % dryrun)
        print(' done')
        return

    def get_image_id(self, image_name):
        for image in self.client.images():
            gotit = False
            for RepoTags in image.get('RepoTags'):
                if RepoTags in image_name:
                    gotit = True
            if gotit:
                return image.get('Id')
        raise Exception('id not found for image name: %s' % image_name)

    def tag_image(self, dryrun=None, **kwargs):
        '''
        tag an image_id using repository and tag
        Examples:
        tag sha256:61ec7424ffa5937ta4a7d377n435702fcs1033c86df343f16645a68765168f92
        repository registry.mycompany.xyz:5000/application/awesomebot
        tag 3.30-1234567
        '''
        image_id = kwargs.get('image_id')
        repository = kwargs.get('repository')
        tag = kwargs.get('tag')
        print('tagging image: id: %s, repository: %s, tag: %s' % (image_id,
                                                                  repository,
                                                                  tag))
        if dryrun is None or dryrun is 0:
            self.client.tag(image_id, repository, tag)
        else:
            print('tag_image -- dryrun: %s' % dryrun)
        return


    def push_image(self, image, dryrun=None):
        '''
        push an image to remote repository, it's a wrapper ;)
        '''
        print('pushing image: %s' % image)
        res = []
        # Aweful trick perhaps here is better some decorator
        if dryrun is None or dryrun is 0:
            for line in self.__primitive_push_image__(image,
                                                      self.destination_registry):
                self.__print_dot__()
                self.__steamerror__(line)
        else:
            print('push_image: -- dryrun: %s' % dryrun)
        print(' done')
        return

    def image_name(self, image):
        name = {}
        # This is not the best...
        regex = '([a-zA-z\.\-]*)(:*)([0-9]*)(/[a-zA-Z0-9\.\/\-\_]*)(:)(.+)'
        try:
            m = re.search(regex, image)
            name = '{"registry": "%s", "port": "%s", "repository": "%s", "tag": "%s"}' % (m.group(1),
                                                                                          m.group(3),
                                                                                          m.group(4),
                                                                                          m.group(6))
            return json.loads(name)
        except Exception as e:
            print('Error parsing image name: %s' % e)


    def delete_image(self, image, dryrun=None, force_delete=True):
        '''
        delete an image from local docker, yet another wrapper...
        '''
        print('removing image: %s' % image)
        if dryrun is None or dryrun is 0:
            print force_delete
            self.client.remove_image(image, force=force_delete)
            return
        else:
            print('delete_image -- dryrun: %s' % dryrun)
        return


# docker = Docker_tool()
# tag = 'registry.mycompany.xyz:5000/application/awesomebot'
# res = docker.pull_image(tag)
# print(docker.get_image_id(tag))
# docker tag sha256:60eb7621faa5937aajkljd311a435202fca10433a84cc333f17645a48761166f32 10.10.10.10:30000/application/awesomebot:3.30-1234
