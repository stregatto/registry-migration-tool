from kubernetes import client, config

class K8sTool(object):
    '''
    Yet another wrapper for kubernetes library plus some glue to simplify the work
    '''

    def __init__(self):
        config.load_kube_config()
        self.k8s_beta = client.ExtensionsV1beta1Api()

    def get_images_from_all_deployment(self):
        '''
        Returns a list contains all images used by deployments.
        Every image is uniq
        '''
        images=[]
        print('retrive list of images for all deployment')
        list_deployment_for_all_namespaces = self.list_deployment_for_all_namespaces()
        for deployment in list_deployment_for_all_namespaces.items:
            for item in deployment.spec.template.spec.containers:
                images.append(item.image)
        return sorted(set(images))

    def list_deployment_for_all_namespaces(self):
        '''
        Returns all deployment for all namespaces
        '''
        deployments = self.k8s_beta.list_deployment_for_all_namespaces()
        return deployments


# k8s_tool = K8s()
# print(k8s_tool.get_images_from_all_deployment())
