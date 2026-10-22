# codeBeamer Python API Wrapper
* TODO: Badges

# Rewrite Branch
This branch is for rewriting my original start of this API wrapper to the service based approach that I saw in [stellaf's](https://github.com/stellaf) fork of the library. It aims to thin the `Codebeamer` class to just hold the client and a number of services that expose similar groupings of API endpoints (such as all `/v3/projects` endpoints in the `ProjectService` class). The goals of this branch are as follows:
- Restructure the project to include a `setup.py` for installing via `pip` (done)
- Implement the skeleton of all the `*Service` classes (done)
- Move existing models into a `models` module (done)
- Implement rework the existing models to the new lazy loading method
- Rework existing models to defer additional API calls to relevant services
- Move existing implemented endpoints from `Codebeamer` class to the relavent services
- Skeleton out all additional models the library needs

Things that are not a goal of this branch but will be worked on after this one is merged to trunk:
- Implementing all the endpoints
- Implementing all the models

## What is it?
The **pybeamer** library provides a **simple** way to interact with codeBeamer's REST API using Python. It is based on codeBeamer's swagger v3 version of the API.

## How to Install?
From PyPi
* Need to figure this out

From GitHub
`pip install -U git+https://github.com/austinmh12/pybeamer.git`

## Examples
More examples to come in the future.

But here's a short example of how to edit a tracker item's summary
```python
from pybeamer import Codebeamer

codebeamer = Codebeamer(
	url = 'http://localhost',
	username='user',
	password='pass'
)

item = codebeamer.get_item(123)
summary = item.get_field('Summary')
summary.value = 'New Summary'
```

The entire codeBeamer space is able to be looked through if an item, tracker, or project is not known by name or ID.
```python
from pybeamer import Codebeamer

codebeamer = Codebeamer(
	url = 'http://localhost',
	username='user',
	password='pass'
)

projects = codebeamer.get_projects()
trackers = projects[0].get_trackers()
items = trackers[0].get_items()
```

The library supports pagination through the API, but by default greedily fetch everything unless a page is specified. By default the `page_size` parameter on all functions that support it is 25 and the codeBeamer API supports any value between 1 and 500. The library will clamp the value passed to these functions.
```python
from pybeamer import Codebeamer

codebeamer = Codebeamer(
	url = 'http://localhost',
	username='user',
	password='pass'
)

# only fetch 10 users
users = codebeamer.get_users(page=1, page_size=10) 
# fetch all users with minimal rest calls
users = codebeamer.get_users(page_size=500)
```

The library also employs a number of helpful features not present in the API, such as fetching projects and trackers by name or ID.
```python
from pybeamer import Codebeamer

codebeamer = Codebeamer(
	url = 'http://localhost',
	username='user',
	password='pass'
)

project_by_id = codebeamer.get_project(1)
project_by_name = codebeamer.get_project('Project')
```

## API Endpoint Progress
These are all the endpoints listed in swagger file for the version of Codebeamer that I have access to (2.2.0.1). The REST API is v3.

Endpoints that have a function listed below them have at least a skeleton, endpoints that are ~~struck out~~ are fully implemented and tested.

### Associations
* POST /associations
* DELETE /associations/{associationId}
* GET /associations/{associationId}
* PUT /associations/{associationId}
* GET /associations/{associationId}/history
* GET /associations/types
* GET /associations/types/{associationTypeId}

### Attachments
* DELETE /attachments/{attachmentId}
* GET /attachments/{attachmentId}
* GET /attachments/{attachmentId}/content
* PUT /attachments/{attachmentId}/content
* GET /attachments/{attachmentId}/history
* PUT /attachments/{attachmentId}/restore

### Baselines
* POST /baselines

### Branches
* GET /branches/{branchId}/item

### Deployment
* POST /deployment
* POST /deployment/export

### Export
* POST /export/items
* POST /export/tracker-item-reviews
* POST /projects/{projectId}/content

### Tracker Item Attachment
* DELETE /items/{itemId}/attachments
* GET /items/{itemId}/attachments
* POST /items/{itemId}/attachments
* DELETE /items/{itemId}/attachments/{attachmentId}
* GET /items/{itemId}/attachments/{attachmentId}
* GET /items/{itemId}/attachments/{attachmentId}/content
* PUT /items/{itemId}/attachments/{attachmentId}/content
* GET /items/{itemId}/attachments/content
* POST /items/attachments/content

### Tracker Item
* DELETE /items/{itemId}
* ~~GET /items/{itemId}~~ 
  * `Codebeamer.get_tracker_item()`
  * `Codebeamer.get_item()`
* PUT /items/{itemId}
* ~~GET /items/{itemId}/children~~ 
  * `TrackerItem.get_children()`
  * `TrackerItem.children`
* PATCH /items/{itemId}/children
* POST /items/{itemId}/children
* PUT /items/{itemId}/children
* ~~GET /items/{itemId}/fields~~
  * `TrackerItem.get_fields()`
  * `TrackerItem.get_field()`
* ~~PUT /items/{itemId}/fields~~
  * `Field.value = 'val'`
* ~~GET /items/{itemId}/fields/{fieldId}/options~~
  * `ChoiceField.get_options()`
* GET /items/{itemId}/fields/accessibility
* PUT /items/{itemId}/fields/tables/{tableFieldId}
* GET /items/{itemId}/history
* DELETE /items/{itemId}/lock
* GET /items/{itemId}/lock
* PUT /items/{itemId}/lock
* GET /items/{itemId}/relations
* GET /items/{itemId}/reviews
* GET /items/{itemId}/transitions
* PUT /items/fields
* GET /items/query
* POST /items/query
* POST /items/relations
* GET /trackers/{trackerId}/children
* PATCH /trackers/{trackerId}/children
* POST /trackers/{trackerId}/children
* PUT /trackers/{trackerId}/children
* POST /trackers/{trackerId}/items

### Tracker Item Comment
* DELETE /items/{itemId}/comments
* GET /items/{itemId}/comments
* POST /items/{itemId}/comments
* DELETE /items/{itemId}/comments/{commentId}
* GET /items/{itemId}/comments/{commentId}
* POST /items/{itemId}/comments/{commentId}
* PUT /items/{itemId}/comments/{commentId}

### Background Job
* GET /job/{jobId}
* POST /jobs/working-set-update

### Migration
* POST /migration/attachment

### Projects
* ~~GET /projects~~
  * `Codebeamer.projects.get_projects()`
  * `Codebeamer.projects()`
* ~~GET /projects/{projectId}~~
  * `Codebeamer.projects.get_project()`
  * `Codebeamer.projects(project=)`
  * `Codebeamer.projects.get_by_id()`
  * `Codebeamer.projects.get_by_name()`
* GET /projects/{projectId}/members
  * `Codebeamer.projects.get_members()`
  * `Codebeamer.projects.get_member()`
  * `Codebeamer.projects.get_member_by_id()`
  * `Codebeamer.projects.get_member_by_name()`
* GET /projects/{projectId}/members/{userId}/permissions
  * `Codebeamer.projects.get_member_project_permissions()`
* ~~GET /projects/{projectId}/trackers~~
  * `Project.get_trackers()`
  * `Project.get_tracker()`
* POST /projects/{projectId}/trackers
  * `Codebeamer.projects.create_tracker()`
* POST /projects/{projectId}/trackers/search
  * `Codebeamer.projects.search_trackers()`
* GET /projects/{projectId}/wikipages
  * `Codebeamer.projects.get_wiki_pages()`
* POST /projects/deploy
  * `Codebeamer.projects.deploy_configuration()`
* ~~POST /projects/search~~
  * `Codebeamer.projects.get_by_key()` which is all this endpoint does

### Wiki
* POST /projects/{projectId}/wiki2html
* POST /wikipages
* PUT /wikipages/{itemId}
* DELETE /wikipages/{wikiId}
* GET /wikipages/{wikiId}
* GET /wikipages/{wikiId}/history
* GET /wikipages/{wikiId}/html
* DELETE /wikipages/{wikiId}/lock
* GET /wikipages/{wikiId}/lock
* PUT /wikipages/{wikiId}/lock
* GET /wikipages/{wikiId}/permissions
* PUT /wikipages/{wikiId}/permissions
* PUT /wikipages/{wikiId}/restorecontent

### Reports
* POST /reports
* PUT /reports/{reportId}
* GET /reports/{reportId}/items
* GET /reports/{reportId}/results

### Roles
* GET /roles
* GET /roles/{roleId}

### System
* GET /system/maintenance
* PUT /system/maintenance

### Test Management
* POST /testcases/autoApplyStepReuses

### Test Runs
* PUT /testruns/{testRunId}
* POST /trackers/{testRunTrackerId}/automatedtestruns
* POST /trackers/{testRunTrackerId}/testruns
* POST /trackers/{testRunTrackerId}/testruns/generatefromtestset

### Traceability
* POST /traceability/items
* POST /traceability/relations

### Tracker Permissions
* GET /trackers/{trackerId}/permissions
* DELETE /trackers/{trackerId}/roles/{roleId}/permissions
* PUT /trackers/{trackerId}/roles/{roleId}/permissions
* GET /trackers/permissions
* GET /trackers/permissions/{trackerPermissionId}

### Tracker
* DELETE /trackers/{trackerId}
* ~~GET /trackers/{trackerId}~~
  * `Codebeamer.get_tracker()`
  * `Project.get_tracker()`
* PUT /trackers/{trackerId}
* GET /trackers/{trackerId}/baselines
* ~~GET /trackers/{trackerId}/fields~~
  * `Tracker.get_fields()`
* ~~GET /trackers/{trackerId}/fields/{fieldId}~~
  * `Tracker.get_field()`
* GET /trackers/{trackerId}/fields/{fieldId}/options/{optionId}
* GET /trackers/{trackerId}/fields/{fieldId}/permissions
* GET /trackers/{trackerId}/fields/permissions
* PUT /trackers/{trackerId}/icon
* ~~GET /trackers/{trackerId}/items~~
  * `Tracker.get_tracker_items()`
  * `Tracker.get_items()`
* GET /trackers/{trackerId}/outline
* GET /trackers/{trackerId}/schema
* GET /trackers/{trackerId}/transitions
* GET /trackers/types
* GET /trackers/types/{trackerTypeId}

### Tracker Report
* GET /trackers/{trackerId}/reports
* POST /trackers/{trackerId}/reports
* DELETE /trackers/{trackerId}/reports/{reportId}
* PUT /trackers/{trackerId}/reports/{reportId}
* GET /trackers/{trackerId}/reports/{reportId}/items
* GET /trackers/{trackerId}/reports/{reportId}/results

### Users
* ~~GET /users~~
  * `Codebeamer.get_users()`
* ~~GET /users/{userId}~~
  * `Codebeamer.get_user()`
* ~~GET /users/findByEmail~~
  * `Codebeamer.get_user()`
* ~~GET /users/findByName~~
  * `Codebeamer.get_user()`
* POST /users/search

### Groups
* GET /users/groups
* GET /users/groups/{groupId}
* GET /users/groups/{groupId}/members

### Wiki Comments
* GET /wikipages/{wikiId}/attachments
* POST /wikipages/{wikiId}/comments