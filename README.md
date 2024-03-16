# Ignition Project Versioning

This readme aims to describe and walkthrough the necessary parts of this repo that will allow for an entire Ignition gateway to be version controlled.

### Important Repos to Visit

| Repositories | Description |
| --- | --- |
| [ignition-k8s](https://github.com/nburnet1/ignition-k8s) | Where we leverage orchestration and containerization |
| [backups](https://github.com/nburnet1/backups) | Where the backups live that we use as gold images |

### Resources

[Ignition 8 Best Practices](https://inductiveautomation.com/resources/article/ignition-8-deployment-best-practices)

[Kevin Collin's ICC Repo](https://github.com/thirdgen88/icc2023-ignition-k8s)

## Overview

### `.scripts/`
Baked into this repo are automatic git commands that are referenced by the projects. By looking in the `.scripts` folder, we can see that there are some shell files containing git commits, pushes, cleans, and restores.

### `.tags/`
The tags directory contains the real-time tags for the entire gateway. In order for this to work, there are some conventions in place. By going into the `.tags` folder, we can see the list of versioned tag providers and the only thing in their directory is a `tags.json`. This is how the gateway reads and inserts the most up-to-date tags.

*Example:*
Path: `.tags/Some_Tags/tags.json`
Tag Provider: `Some_Tags`
Backup: `tags.json`

### Projects
While you can follow any kind of project structure, here are some important notes that allow for automatic pushes.

For each project that we want to be versioned on save, we would put an update script along the lines of:

```python
import time
time.sleep(5)
system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-auto-commit.sh"])
```

*Note on Automatic Tag Exports*

In the same script where the auto commit lives, we can also place a tag export above before we commit.

```python
filePath = "/usr/local/bin/ignition/data/projects/.tags/Some_Tags/tags.json"
tags = system.tag.exportTags(filePath=filePath, tagPaths=["[Some_Tags]"], recursive=True)
```

While this repo aims to automate the versioning of the project as much as possible, it will need to be paired with a backup ([See backup repo](https://github.com/nburnet1/backups)) in order to persist any gateway changes. Additionally, to ensure a clean and consistent environment, using containerization is the best approach. By looking at the [ignition-k8s](https://github.com/nburnet1/ignition-k8s) repo, there are many problems solved by taking the containerization approach.
