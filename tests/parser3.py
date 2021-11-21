
import datetime
import releasy

miner = releasy.Miner()
project = miner.mine(path="/mnt/d/repos/research/release/repos/d3/d3")

print(f"{len(project.main_releases):4} - {project.datasource.vcs.path}")
print(f"{'release':10} {'base':10} {'# commits':>10} {'delay':10}")
rapid_releases = set()
trad_releases = set()
for main_release in project.main_releases:
    try:
        release_name = main_release.name
        commits = '' 
        if main_release.commits:
            commits = len(main_release.commits)
        if main_release.base_main_release:
            base_release_name = main_release.base_main_release.name
            release_delay = str(main_release.delay)
            if main_release.delay <= datetime.timedelta(days=7*6):
                rapid_releases.add(main_release)
            if main_release.delay >= datetime.timedelta(days=7*12):
                trad_releases.add(main_release)
        else: 
            base_release_name = "None"
            release_delay = "None"

        print(f"{release_name:10} {base_release_name:10} {commits:>10} {release_delay:10}")
    except Exception as e: 
        pass
        #print(main_release.name, e)
        #print(traceback.format_exc())
print(f"Releases: {len(project.main_releases):5} Rapid: {len(rapid_releases):5} Traditional: {len(trad_releases):5}")
