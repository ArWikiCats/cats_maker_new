# Refactoring and Testing Plan

## Introduction

The purpose of this document is to outline a comprehensive testing plan to ensure that all functionality of the codebase remains correct and robust after a significant refactoring effort. The primary goal is to establish a suite of tests that covers all critical parts of the application, allowing for confident and safe code modifications in the future.

This plan details the modules to be tested, the priority of testing for each module, and the modules that are explicitly excluded from this testing plan.

## High-Priority Modules

The following modules are considered critical to the application and should be prioritized for testing. For each of these modules, a comprehensive suite of unit and integration tests should be developed to cover all public functions and methods.

### `src/b18_new`

- **Objective:** Ensure all functions in the `b18_new` module are thoroughly tested.
- **Methodology:** Write unit tests for each individual function, mocking any external dependencies. Write integration tests to verify the interactions between functions within this module.

### `src/mk_cats`

- **Objective:** Verify the correctness of all functionality within the `mk_cats` module.
- **Methodology:** Create a series of tests that cover all logic paths within the module. Pay special attention to edge cases and boundary conditions.

### `src/c18_new`

- **Objective:** Achieve complete test coverage for the `c18_new` module.
- **Methodology:** Develop a combination of unit and integration tests. Ensure that all data transformations and manipulations are tested thoroughly.

### `src/api_sql`

- **Objective:** Validate the functionality of the `api_sql` module, particularly its interactions with the database.
- **Methodology:** Write tests that mock the database interactions to test the business logic in isolation. Additionally, write integration tests that run against a test database to ensure the SQL queries and transactions are correct.

## Other Modules

The following modules should also be tested to ensure full coverage of the application.

### `src/helps`, `src/temp`, `src/textfiles`, `src/utils`, `src/wiki_api`

- **Objective:** Ensure that all functions within these modules are tested.
- **Methodology:** For each module, write unit tests for all public functions. Ensure that any file I/O operations are properly mocked and tested.

## Excluded Modules

The following modules are explicitly excluded from this testing plan:

- `src/new_api`
- `src/wd_bots`
