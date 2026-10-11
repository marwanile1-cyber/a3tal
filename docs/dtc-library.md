# Independent DTC library

`/dtc/` and existing published DTC guide URLs use scoped templates from A3tal
Global. The library deduplicates existing structured records and category 2
guides by code. It does not scrape another publisher or move articles.

Anonymous questions and replies are native WordPress comments held for review.
Moderate them in WordPress → Comments. Optional vehicle details and report
counts appear in the comment editor. Reports do not auto-hide other visitors.
There is no email requirement, mailing flow, or account signup.

Deploy from the private `a3tal-control` repository, whose DTC workflow invokes
the source workflow here at a pinned reviewed commit and passes the existing
`A3TAL_CONTROL_SECRET`. This source workflow is reusable; it never deploys on
an ordinary source push with an obsolete public-repository secret.

The workflow saves an encrypted artifact before live writes, lints the actual
live functions candidate, compares original hashes to prevent conflicts,
reads every uploaded file back, and activates the helper last. All new files
use existing server directories. Existing templates are preserved.

Run the control workflow with `mode=deactivate` to remove only the marked
include from live functions. This restores the existing templates and keeps
articles and comments. Source updates while the library is active are rejected;
deactivate first, deploy the new pinned source, then complete public QA.

Encrypted backup artifacts expire after seven days. They can be decrypted in a
trusted environment using OpenSSL AES-256-CBC/PBKDF2, 200000 iterations, and the
same protected bridge secret. Do not publish plaintext originals or credentials.
