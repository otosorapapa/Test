import os
import shutil
import zipfile
import hashlib
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    base_dir = root / "keiei_exam_app_pro_v17_all"
    zip_path = root / "keiei_exam_app_pro_v17_all.zip"

    # Clean previous outputs
    if base_dir.exists():
        shutil.rmtree(base_dir)
    if zip_path.exists():
        zip_path.unlink()

    # Directories/files to include
    files = ["README.md", "app.py", "requirements.txt"]
    dirs = ["pages", "utils", "data", "export", "static", ".streamlit"]

    # Create base directory
    base_dir.mkdir(parents=True)

    for f in files:
        shutil.copy2(root / f, base_dir / f)
    for d in dirs:
        shutil.copytree(root / d, base_dir / d)

    # Best-effort copy user's PDFs and DOCXs from /mnt/data
    src = Path("/mnt/data")
    pp_dest = base_dir / "data" / "past_papers"
    docs_dest = base_dir / "data" / "docs"
    pp_dest.mkdir(parents=True, exist_ok=True)
    docs_dest.mkdir(parents=True, exist_ok=True)

    for p in src.glob("*.pdf"):
        try:
            if p.stat().st_size < 100 * 1024 * 1024:
                shutil.copy2(p, pp_dest / p.name)
        except FileNotFoundError:
            pass
    for dfile in src.glob("*.docx"):
        try:
            if dfile.stat().st_size < 100 * 1024 * 1024:
                shutil.copy2(dfile, docs_dest / dfile.name)
        except FileNotFoundError:
            pass

    # Bundle convenience zips
    bundle_pp = base_dir / "data" / "past_papers_bundle.zip"
    with zipfile.ZipFile(bundle_pp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in pp_dest.glob("*.pdf"):
            zf.write(p, p.name)

    bundle_docs = base_dir / "data" / "docs_bundle.zip"
    with zipfile.ZipFile(bundle_docs, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in docs_dest.glob("*.docx"):
            zf.write(p, p.name)

    # Build final zip
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in base_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(base_dir).as_posix())

    sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    file_count = sum(len(files) for _, _, files in os.walk(base_dir))
    pdf_count = len(list(pp_dest.glob("*.pdf")))
    docx_count = len(list(docs_dest.glob("*.docx")))

    summary = {
        "zip_path": str(zip_path),
        "sha256": sha,
        "file_count": file_count,
        "pdf_count": pdf_count,
        "docx_count": docx_count,
    }
    print(summary)


if __name__ == "__main__":
    main()
