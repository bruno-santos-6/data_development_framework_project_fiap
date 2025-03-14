# data_development_framework_project_fiap

+-------------------+     +-------------------+     +-------------------+
|    Azure VM Dev   |     |  Azure Kubernetes |     |  Azure SQL DB     |
|  (Docker, Git)    | --> |  Service (AKS)    | --> |  & Data Lake Gen2 |
+-------------------+     +-------------------+     +-------------------+
       |                        |
       |    +-------------+     |
       +--> | Container   |     |
            | Registry   | <---+
            +------------+