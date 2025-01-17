// Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
// conditions defined in the file COPYING, which is part of this source code package.

use anyhow::Result;
/// Platform independent file and time routines
use std::fs;
use std::path::{Path, PathBuf};
use std::time::UNIX_EPOCH;

pub fn touch_dir<P: AsRef<Path>>(path: P) -> Result<PathBuf> {
    fs::File::create(path.as_ref().join(".touch"))?;
    fs::remove_file(path.as_ref().join(".touch"))?;
    Ok(path.as_ref().to_path_buf())
}

fn get_modified_utc_time<P: AsRef<Path>>(path: P) -> Result<u64> {
    Ok(fs::metadata(path)?
        .modified()?
        .duration_since(UNIX_EPOCH)?
        .as_secs())
}

pub fn get_utc_now() -> Result<u64> {
    Ok(std::time::SystemTime::now()
        .duration_since(UNIX_EPOCH)?
        .as_secs())
}

pub fn get_modified_age<P: AsRef<Path>>(path: P) -> Result<u64> {
    let modified = get_modified_utc_time(path)?;
    let now = get_utc_now()?;
    Ok(if now >= modified { now - modified } else { 0 })
}

#[cfg(test)]
mod tests {
    use super::get_modified_utc_time;

    #[test]
    fn test_get_utc_modified_time() {
        let e = get_modified_utc_time(".").unwrap();
        assert!(e > 1700000000);
    }
}
