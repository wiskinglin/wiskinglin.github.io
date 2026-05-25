# Implementation Plan - Deploy dev to main

This plan outlines the steps for merging the `dev` branch to the `main` branch, updating the release notes, and pushing the changes to the production server.

## Stage 1: Document Release Notes in `new.html`
**Goal**: Update `new.html` with recent developments including menu tool component, GitHub Ecosystem layout optimization, and general clean-ups.
**Success Criteria**: `new.html` contains the updated list of changes under the latest date section (2026-05-25).
**Tests**: Check if `new.html` renders correctly without broken syntax.
**Status**: Complete

## Stage 2: Commit Release Notes on `dev`
**Goal**: Commit the changes to `new.html` in the `dev` branch.
**Success Criteria**: Git status is clean and the new release notes commit is added.
**Tests**: `git status` shows no modified files on `dev`.
**Status**: Complete

## Stage 3: Merge `dev` into `main` excluding `_data`
**Goal**: Merge `dev` to `main` while discarding/excluding `_data` updates from the commit on `main`.
**Success Criteria**: Successfully checkout to `main`, run merge with `--no-commit --no-ff`, untrack and remove `_data`, and complete the merge commit.
**Tests**: `git status` on `main` is clean, and the files in `_data` are not present on `main` workspace.
**Status**: In Progress

## Stage 4: Deploy (Push) to Remote Repository
**Goal**: Push `main` and `dev` branches to the remote repository.
**Success Criteria**: Both branches pushed successfully to origin.
**Tests**: `git push origin main` and `git push origin dev` complete without errors.
**Status**: Not Started
