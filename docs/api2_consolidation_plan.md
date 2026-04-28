# api2 — Consolidation Plan

> Consolidate `WikiApiClient`, `Login`, `Transport`, and `AuthProvider` into a clean layered architecture.

---

## 1. Current State

`WikiApiClient`, `Transport`, and `AuthProvider` were split from the original `bot.py`. However:

-   **`WikiApiClient`** is the **only class actively used** — `Login` wraps it as `self._client`
-   **`Transport`** is **never imported** by any consumer
-   **`AuthProvider`** is **never imported** by any consumer

This means `Transport` and `AuthProvider` exist but are unreachable dead code. Meanwhile `Login` duplicates many methods that already exist in `WikiApiClient`.

---

## 2. Duplication Map

### WikiApiClient owns (and Login duplicates):

| Method               | Location                                                     |
| -------------------- | ------------------------------------------------------------ |
| `filter_params`      | `client.py:110`, `super_login.py:69`                         |
| `p_url`              | `client.py:123`, `super_login.py:82`                         |
| `make_response`      | `client.py:135`, `super_login.py:101`                        |
| `post_params`        | `client.py:231`, `super_login.py:227`                        |
| `_make_new_r3_token` | `client.py:266`, `super_login.py:443`                        |
| `_error_do`          | `client.py:277`, `super_login.py` (inlined at lines 261-285) |
| `post_it_parse_data` | `client.py:202`, `super_login.py:203`                        |
| `params_w`           | `client.py:53`, also `params_help.py`                        |
| `parse_data`         | `client.py:79`, also `params_help.py`                        |

### Login duplicates Transport:

| Method                 | Location                                 |
| ---------------------- | ---------------------------------------- |
| `post_it`              | `transport.py:100`, `super_login.py:125` |
| `_raw_request`         | `transport.py:58`, `super_login.py:154`  |
| `_make_session`        | `transport.py:44`, `super_login.py:146`  |
| `_handle_server_error` | `transport.py:95`, `super_login.py:198`  |

### Login duplicates AuthProvider:

| Method               | Location                                              |
| -------------------- | ----------------------------------------------------- |
| `log_in`             | `auth.py:40`, `super_login.py:320`                    |
| `_get_logintoken`    | `auth.py:49`, `super_login.py:338`                    |
| `_get_login_result`  | `auth.py:76`, `super_login.py:366`                    |
| `_logged_in`         | `auth.py:118`, `super_login.py:409`                   |
| `_make_new_r3_token` | `auth.py:149`, `super_login.py:443`                   |
| `ensure_logged_in`   | `auth.py:175`, `super_login.py:475`                   |
| `add_User_tables`    | `auth.py:164`, `super_login.py:60`                    |
| `add_users`          | `super_login.py:54` (calls `_client.add_User_tables`) |

---

## 3. Target Architecture

```
Login
├── _transport: Transport     (session, raw_request, post_it, params_w, parse_data)
├── _auth: AuthProvider        (log_in, tokens, add_User_tables, ensure_logged_in)
├── post_params                (iterative retry loop — own logic)
├── handle_err                (inherited from HandleErrors)
└── add_users                  (delegates to _auth)
```

`WikiApiClient` is deleted — its methods are absorbed:

-   HTTP/session logic → `Transport`
-   Auth/token logic → `AuthProvider`
-   Param manipulation → `Transport.params_w` (or standalone helper)

---

## 4. Execution Steps

### Step 1 — Make Login Fully Delegate to WikiApiClient

**Goal:** Remove all duplicated methods from `Login` that already exist in `WikiApiClient`.

| Method to DELETE from Login | Reason                                                |
| --------------------------- | ----------------------------------------------------- |
| `filter_params`             | Duplicates `WikiApiClient.filter_params`              |
| `p_url`                     | Duplicates `WikiApiClient.p_url`                      |
| `make_response`             | Duplicates `WikiApiClient.make_response`              |
| `_make_response_impl`       | Same logic as `WikiApiClient.make_response`           |
| `post_it`                   | Uses same session pattern as WikiApiClient            |
| `_raw_request`              | Duplicates `Transport._raw_request` logic             |
| `_make_session`             | `WikiApiClient.__init__` already calls `load_session` |
| `_handle_server_error`      | Duplicates `Transport._handle_server_error`           |
| `post_params`               | Duplicates `WikiApiClient.post_params`                |
| `_error_do`                 | Logic inlined in `WikiApiClient._error_do`            |

**Keep in Login after Step 1:**

-   `log_in`, `_get_logintoken`, `_get_login_result`, `_logged_in`
-   `_make_new_r3_token`, `ensure_logged_in`
-   `add_users`, `add_User_tables`
-   `make_new_session`, `session` property

**Implementation:**

1. Change all calls from `self.X()` to `self._client.X()` for deleted methods
2. `post_it` → replaced with `self._client.session.request("POST", ...)`
3. Remove all import of `transport` and `cookies_bot` from `super_login.py`
4. Verify tests still pass

**Result:** `Login` still wraps `WikiApiClient` but with no duplicate methods (~350 lines).

---

### Step 2 — Make Login Use Transport and AuthProvider

**Goal:** Replace the `WikiApiClient` wrapper with composed `Transport` + `AuthProvider`.

| Login method                                 | Delegates to                                                 |
| -------------------------------------------- | ------------------------------------------------------------ |
| `log_in`                                     | `AuthProvider.log_in`                                        |
| `_get_logintoken`                            | `AuthProvider._get_logintoken`                               |
| `_get_login_result`                          | `AuthProvider._get_login_result`                             |
| `_logged_in`                                 | `AuthProvider._logged_in`                                    |
| `_make_new_r3_token`                         | `AuthProvider._make_new_r3_token`                            |
| `ensure_logged_in`                           | `AuthProvider.ensure_logged_in`                              |
| `add_users` / `add_User_tables`              | `AuthProvider.add_User_tables`                               |
| `make_new_session`                           | `AuthProvider.ensure_logged_in` + cookie persistence         |
| `post_it` / `_raw_request` / `_make_session` | `Transport.post_it` / `Transport._raw_request`               |
| `params_w`                                   | Standalone helper (or `Transport.params_w` if moved there)   |
| `parse_data`                                 | Standalone helper (or `Transport.parse_data` if moved there) |

**Implementation:**

1. Add `self._transport = Transport(...)` in `Login.__init__`
2. Add `self._auth = AuthProvider(...)` in `Login.__init__`
3. Wire: `AuthProvider.session = self._transport.session`
4. Replace all `self._client.X` with `self._transport.X` or `self._auth.X`
5. `WikiApiClient` is no longer instantiated in `Login.__init__`
6. Delete `client.py`
7. Move `WikiApiClient.params_w` and `WikiApiClient.parse_data` to standalone helpers or `Transport`

**Result:** `Login` uses `Transport` + `AuthProvider`, no `WikiApiClient` exists.

---

### Step 3 — Merge Transport/Login Duplicate Functions

**Goal:** Remove remaining overlap between `Login` and `Transport`.

| Duplicate pair                                                  | Action                                                      |
| --------------------------------------------------------------- | ----------------------------------------------------------- |
| `Transport.post_it` / `Login.post_it`                           | `Login.post_it` → `return self._transport.post_it(...)`     |
| `Transport._raw_request` / `Login._raw_request`                 | DELETE from `Login` — use `_transport._raw_request`         |
| `Transport._make_session` / `Login._make_session`               | DELETE from `Login` — `Transport._make_session` handles it  |
| `Transport._handle_server_error` / `Login._handle_server_error` | DELETE from `Login` — use `_transport._handle_server_error` |

**Implementation:**

-   `Login.post_it` becomes: `return self._transport.post_it(params, files, timeout)`
-   All HTTP-level logic lives in `Transport` only
-   Remove `_raw_request`, `_make_session`, `_handle_server_error` from `Login`

---

### Step 4 — Merge AuthProvider/Login Duplicate Functions

**Goal:** Remove remaining overlap between `Login` and `AuthProvider`.

| Duplicate pair                                                 | Action                                        |
| -------------------------------------------------------------- | --------------------------------------------- |
| `AuthProvider.log_in` / `Login.log_in`                         | `Login.log_in` → `return self._auth.log_in()` |
| `AuthProvider._get_logintoken` / `Login._get_logintoken`       | DELETE from `Login`                           |
| `AuthProvider._get_login_result` / `Login._get_login_result`   | DELETE from `Login`                           |
| `AuthProvider._logged_in` / `Login._logged_in`                 | DELETE from `Login`                           |
| `AuthProvider._make_new_r3_token` / `Login._make_new_r3_token` | DELETE from `Login`                           |
| `AuthProvider.ensure_logged_in` / `Login.ensure_logged_in`     | DELETE from `Login`                           |
| `AuthProvider.add_User_tables` / `Login.add_User_tables`       | DELETE from `Login`                           |
| `AuthProvider.add_users` / `Login.add_users`                   | DELETE from `Login`                           |

**Implementation:**

-   Every `Login.X` that mirrors `AuthProvider.X` becomes `return self._auth.X(...)` or is deleted
-   `Login` keeps only `post_params` (retry loop) and `add_users` (orchestration)
-   All auth logic lives in `AuthProvider` only

---

## 5. Final File Structure

```
src/core/api2/super/
├── __init__.py
├── all_apis.py
├── auth.py               # AuthProvider — USED (login, tokens, add_User_tables, ensure_logged_in)
├── transport.py          # Transport — USED (session, raw_request, post_it, params_w, parse_data)
├── super_login.py        # Login = Transport + AuthProvider composition
├── super_page.py
├── catdepth_new.py
├── cookies_bot.py
├── handel_errors.py
├── params_help.py
└── models.py

client.py    → DELETED  (WikiApiClient absorbed into Transport + AuthProvider)
```

---

## 6. Acceptance Criteria

-   [ ] `Login` has **no method** that duplicates any method in `Transport` or `AuthProvider`
-   [ ] `Login` holds `self._transport: Transport` and `self._auth: AuthProvider`
-   [ ] All HTTP operations go through `Transport`
-   [ ] All auth operations (login, tokens) go through `AuthProvider`
-   [ ] `client.py` is deleted
-   [ ] `pytest tests/api2/` passes
-   [ ] `ruff check src/core/api2` passes
-   [ ] `mypy src/core/api2 --ignore-missing-imports` passes

---

_Plan created 2026-04-27._
