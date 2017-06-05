import docker
import re

class Docker_tool(object):
    '''
    More or less a wrapper for docker library.
    Here I would like to add some glue to simplify the work
    '''

    def __init__(self):
        self.client = docker.APIClient(base_url='unix://var/run/docker.sock')

    def pull_image(self, image, dryrun=None):

        try:
            print('pulling image: %s' % image)
            if dryrun is 0:
                print('no dry run')
                res = self.client.pull(image)
                return res
        except Exception as e:
            print('Error: %s' % e)

    def get_image_id(self, tag):
        for image in self.client.images():
            gotit = False
            for RepoTags in image.get('RepoTags'):
                if tag in RepoTags:
                    gotit = True
            if gotit:
                return image.get('Id')
        raise Exception('id not found for image tag: %s' % tag)

    def tag_image(self, dryrun=None, **kargs):
        '''
        tag an image_id using repository and tag
        Examples:
        tag sha256:61ec7424ffa5937ta4a7d377n435702fcs1033c86df343f16645a68765168f92
        repository registry.mycompany.xyz:5000/application/awesomebot
        tag 3.30-1234567
        '''
        print('tagging image id %s, repository: %s, tag: %s' % (image_id,
                                                                repository,
                                                                tag))
        if dryrun is 0:
            print('no dry run')
            client.tag(image_id, repository, tag)
        return

    def push_image(self, image, dryrun):
        '''
        push an image to remote repository, it's a wrapper ;)
        '''
        print('pushing image: %s' % image)
        if dryrun is 0:
            print('no dry run')
            # client.push(image)
        return

    def image_name(self, image):
        name = {}
        print image
        # This is not the best...
        regex = '([a-zA-z\.\-]*)(:*)([0-9]*)(/[a-zA-Z0-9\.\/\-\_]*)(:)(.+)'
        try:
            m = re.search(regex, image)
            name = {'registry': m.group(1),
                    'port': m.group(3),
                    'repository': m.group(4),
                    'tag': m.group(5)}
            return json.loads(name)
        except Exception as e:
            print('Error parsing image name: %s' % e)


    def delete_image(self, image, dryrun, force=True):
        '''
        delete an image from local docker, yet another wrapper...
        '''
        print('removing image: %s' % image)
        if dryrun is 0:
            print('no dry run')
            # client.remove_image(image, force)
        return


# docker = Docker_tool()
# tag = 'registry.mycompany.xyz:5000/application/awesomebot'
# res = docker.pull_image(tag)
# print(docker.get_image_id(tag))
# docker tag sha256:60eb7621faa5937aajkljd311a435202fca10433a84cc333f17645a48761166f32 10.10.10.10:30000/application/awesomebot:3.30-1234
