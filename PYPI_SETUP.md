# PyPI Setup Instructions

This document provides instructions for maintaining the PyPI package publication for CACTS.

## Overview of Changes Made

The following changes were made to resolve PyPI warnings:

### 1. Fixed Package Metadata Warnings

**Issue**: Missing `long_description` and `long_description_content_type` warnings during package build.

**Solution**: Updated `pyproject.toml` to include:
- `readme = "readme"` - Points to the readme file for long description
- `license = {file = "license"}` - Points to the license file

These changes ensure that PyPI has proper package metadata and eliminates the warnings about missing long description.

### 2. Updated to Trusted Publishing

**Issue**: Security warnings about using API tokens with attestations enabled.

**Solution**: Updated `.github/workflows/pypi.yaml` to use Trusted Publishing:
- Added `permissions: id-token: write` to the job
- Removed `user` and `password` fields from the publish step
- Added comments explaining the change

## Setting Up Trusted Publishing (Required for Maintainers)

**IMPORTANT**: A repository maintainer with PyPI package owner permissions must complete this setup before the next release.

### Step 1: Configure Trusted Publisher on PyPI

1. Log in to [PyPI](https://pypi.org) as an owner of the `cacts` package
2. Navigate to the specific URL provided in the original warning:
   ```
   https://pypi.org/manage/project/cacts/settings/publishing/?provider=github&owner=E3SM-Project&repository=cacts&workflow_filename=pypi.yaml
   ```
3. Follow the prompts to set up the Trusted Publisher
4. Verify the configuration matches:
   - **Owner**: E3SM-Project
   - **Repository**: cacts
   - **Workflow filename**: pypi.yaml

### Step 2: Remove API Token Secret (After Setup)

Once Trusted Publishing is configured:

1. Go to the repository settings: https://github.com/E3SM-Project/cacts/settings/secrets/actions
2. Delete the `PYPI_API_TOKEN` secret (it's no longer needed)

### Step 3: Test the Setup

The next time a release is published, the workflow will automatically use Trusted Publishing. Monitor the action logs to ensure it works correctly.

## Benefits of Trusted Publishing

- **Enhanced Security**: No long-lived API tokens stored in GitHub secrets
- **Automatic Attestations**: Package authenticity verification
- **Reduced Maintenance**: No need to rotate API tokens
- **Better Audit Trail**: Clear connection between GitHub repository and PyPI package

## Troubleshooting

### If Publishing Fails After Setup

1. Verify the Trusted Publisher configuration on PyPI matches exactly:
   - Owner: `E3SM-Project`
   - Repository: `cacts`
   - Workflow filename: `pypi.yaml`

2. Check that the GitHub Actions workflow has the correct permissions:
   ```yaml
   permissions:
     id-token: write
   ```

3. Ensure no `user` or `password` fields are present in the publish step

### Reverting to API Tokens (Not Recommended)

If you need to temporarily revert to API tokens:

1. Add back the `user` and `password` fields in the workflow
2. Recreate the `PYPI_API_TOKEN` secret
3. Remove the `permissions: id-token: write` line

However, this will bring back the security warnings and is not recommended for long-term use.

## References

- [PyPI Trusted Publishers Documentation](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [PyPA Publish Action Documentation](https://github.com/pypa/gh-action-pypi-publish)