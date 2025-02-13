from pathlib import Path

# Because symlinks on windows require elevated priviledges I decided to just make my own crude version
class PathLink(Path):
    def read_link_path(self) -> Path:
        return Path(self.read_text())
    
    def write_link_path(self, target: Path):
        self.write_text(str(target.absolute()))