# Roles, Moderation, Catalog Plan

## Goal

Add:
- user and admin roles
- admin moderation flow for public recipes
- public catalog for approved recipes
- cloning public recipes into a user's personal cookbook

## Progress

- [x] Create implementation plan file
- [x] Add backend role support
- [x] Add recipe publication and moderation fields
- [x] Add catalog API for approved public recipes
- [x] Add admin moderation API
- [x] Add submit-for-review flow for user recipes
- [x] Add backend tests for roles, moderation, and catalog cloning
- [x] Add frontend role awareness
- [x] Add frontend admin pages
- [x] Show admin/public catalog recipes on the landing page
- [x] Add UI for "submit for review"
- [x] Add UI for "add to my cookbook"

## Implemented Backend Scope

### Users
- `role` field added to users
- `require_admin` dependency added
- `/auth/me` now returns `role`

### Recipes
- publication fields added:
  - `visibility`
  - `publication_status`
  - `is_admin_recipe`
  - `approved_by`
  - `approved_at`
  - `rejection_reason`
  - `original_recipe_id`

### New APIs
- `POST /recipes/{id}/submit-for-review`
- `GET /catalog`
- `GET /catalog/{id}`
- `POST /catalog/{id}/clone`
- `GET /admin/recipes/pending`
- `POST /admin/recipes/{id}/approve`
- `POST /admin/recipes/{id}/reject`
- `POST /admin/recipes`

## Implemented Frontend Scope

- auth store now tracks `role` and `isAdmin`
- admin moderation page added
- catalog list and catalog recipe detail pages added
- landing page now renders admin and community recipes from the API
- personal recipe pages now show publication status and allow review submission
- catalog recipes can be copied into a user's cookbook

## Verification

- `python -m pytest -q` -> `25 passed`
- `npm run build` -> should pass after frontend verification

## Next Recommended Steps

1. Add search and filters to the catalog endpoint and UI.
2. Add admin recipe creation UI.
3. Add moderation history and approval metadata to the frontend.
4. Add better recipe ingredient/step rendering for catalog cards.
5. Add end-to-end frontend tests for moderation and cloning flows.
