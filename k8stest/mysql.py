
from kube import ClientSingleton, CustomResourceClientSingleton
import yaml, time

mysqlyaml ='''
apiVersion: mysql.radondb.com/v1beta1
kind: MysqlCluster
metadata:
  name: sample
spec:
  backupOpts:
    image: radondb/mysql80-sidecar:v3.0.0
    resources:
      requests:
        cpu: 10m
        memory: 32Mi
  customTLSSecret: {}
  dataSource:
    S3backup:
      name: ""
      secretName: ""
    remote: 
      # sourceConfig:
      #     name: remotesecret
      #     items:
      #     - key: passwd
      #       path: passwd
      #     - key: host
      #       path: host
    
  image: percona/percona-server:8.0.25
  imagePullPolicy: Always
  logOpts:
    resources:
      requests:
        cpu: 10m
        memory: 32Mi
  maxLagTime: 30
  minAvailable: 50%
  monitoringSpec:
    exporter:
      enabled: true
      image: prom/mysqld-exporter:v0.12.1
      resources:
        limits:
          cpu: 100m
          memory: 128Mi
        requests:
          cpu: 10m
          memory: 32Mi
  mysqlConfig: {}
  mysqlVersion: "8.0"
  replicas: 3
  resources:
    limits:
      cpu: 500m
      memory: 1Gi
    requests:
      cpu: 100m
      memory: 256Mi
  storage:
    accessModes:
    - ReadWriteOnce
    storageClassName: local-path
    resources:
      requests:
        storage: 20Gi
  user: radondb_usr
  xenonOpts:
    admitDefeatHearbeatCount: 5
    electionTimeout: 10000
    image: radondb/xenon:v3.0.0
    resources:
      limits:
        cpu: 100m
        memory: 256Mi
      requests:
        cpu: 50m
        memory: 128Mi
'''
def createMysqlCluster():
    mysql = yaml.safe_load(mysqlyaml)
    api_instance = CustomResourceClientSingleton()
    api_instance.create_namespaced_custom_object(group="mysql.radondb.com", namespace='default',
                                              version="v1beta1",plural="mysqlclusters", 
                                              body=mysql) 
def deleteMysqlCluster(name):
    api_instance = CustomResourceClientSingleton()
    api_instance.delete_namespaced_custom_object(group="mysql.radondb.com", namespace='default',
                                              version="v1beta1",plural="mysqlclusters", 
                                              name=name)
def waitingMysqlClusterReady(name):
    api_instance = CustomResourceClientSingleton()
    while True:
        try:
            obj = api_instance.get_namespaced_custom_object(group="mysql.radondb.com", namespace='default',
                                                  version="v1beta1",plural="mysqlclusters", 
                                                  name=name)
            print(obj.get('status').get('state'))
            if obj.get('status').get('state') == 'Ready':
              break
            else:
                time.sleep(2)
        except:
            print("waiting mysql cluster ready")
            time.sleep(1)
def patchMysqlCluster(name, body):
    api_instance = CustomResourceClientSingleton()
    return api_instance.patch_namespaced_custom_object(group="mysql.radondb.com", namespace='default',
                                              version="v1beta1",plural="mysqlclusters", 
                                              name=name, body=body)

def labelPod(name, label):
    api_instance = ClientSingleton()
    #print(label)
    return api_instance.patch_namespaced_pod(name=name, namespace='default',
                                              body={'metadata':{'labels':label}})
    
def changeReplica(num):
    mysql = yaml.safe_load(mysqlyaml)
    mysql['spec']['replicas'] = num
    return patchMysqlCluster('sample', mysql)


def rebuildPod(name:str, fromname :str)-> bool:
    try:
        label = {"rebuild": fromname}
        assert labelPod(name, label)
        waitingMysqlClusterReady('sample')
    except Exception as e:
        print(e)
        assert False