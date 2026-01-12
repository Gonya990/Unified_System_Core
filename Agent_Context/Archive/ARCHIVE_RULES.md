# Agent Rules: Archive Directory Management

To preserve the integrity of historical data and audit trails, the following rules apply to the `Agent_Context/Archive/` directory:

1. **No Data Loss**: Never perform any operations that result in the loss of information within the `Archive/` directory.
2. **No Compression**: Do not compress or zip files within the archive. Content must remain in its original, readable format.
3. **Immutability**: Once a file is moved to the `Archive/`, it should be treated as read-only. Avoid modifying the content of archived files.
4. **Metadata Preservation**: Ensure that when moving files to the archive, original context (such as timestamps or session IDs in filenames) is preserved.
5. **No Pruning**: Archived files are excluded from automated cleanup or pruning tasks unless explicitly requested by the user for a specific legal or security reason.
