# coding: utf8
from __future__ import unicode_literals

import plac
import requests
import os
import subprocess
import sys
from wasabi import Printer

from .link import link
from ..util import get_package_path
from .. import about


msg = Printer()


@plac.annotations(
    model=("Model to download (shortcut or name)", "positional", None, str),
    direct=("Force direct download of name + version", "flag", "d", bool),
    pip_args=("additional arguments to be passed to `pip install` on model install"),
)
def download(model, direct=False, *pip_args):
    """
    Download compatible model from default download path using pip. Model
    can be shortcut, model name or, if --direct flag is set, full model name
    with version. For direct downloads, the compatibility check will be skipped.
    """
    if direct:
        dl = download_model("{m}/{m}.tar.gz#egg={m}".format(m=model), pip_args)
    else:
        shortcuts = get_json(about.__shortcuts__, "available shortcuts")
        model_name = shortcuts.get(model, model)
        compatibility = get_compatibility()
        version = get_version(model_name, compatibility)
        dl_tpl = "{m}-{v}/{m}-{v}.tar.gz#egg={m}=={v}"
        dl = download_model(dl_tpl.format(m=model_name, v=version), pip_args)
        if dl != 0:  # if download subprocess doesn't return 0, exit
            sys.exit(dl)
        try:
            # Get package path here because link uses
            # pip.get_installed_distributions() to check if model is a
            # package, which fails if model was just installed via
            # subprocess
            package_path = get_package_path(model_name)
            link(model_name, model, force=True, model_path=package_path)
        except:  # noqa: E722
            # Dirty, but since spacy.download and the auto-linking is
            # mostly a convenience wrapper, it's best to show a success
            # message and loading instructions, even if linking fails.
            msg.warn(
                "Download successful but linking failed",
                "Creating a shortcut link for 'en' didn't work (maybe you "
                "don't have admin permissions?), but you can still load the "
                "model via its full package name: "
                "nlp = spacy.load('{}')".format(model_name),
            )


def get_json(url, desc):
    r = requests.get(url)
    if r.status_code != 200:
        msg.fail(
            "Server error ({})".format(r.status_code),
            "Couldn't fetch {}. Please find a model for your spaCy "
            "installation (v{}), and download it manually. For more "
            "details, see the documentation: "
            "https://spacy.io/usage/models".format(desc, about.__version__),
            exits=1,
        )
    return r.json()


def get_compatibility():
    version = about.__version__
    version = version.rsplit(".dev", 1)[0]
    comp_table = get_json(about.__compatibility__, "compatibility table")
    comp = comp_table["spacy"]
    if version not in comp:
        msg.fail("No compatible models found for v{} of spaCy".format(version), exits=1)
    return comp[version]


def get_version(model, comp):
    model = model.rsplit(".dev", 1)[0]
    if model not in comp:
        msg.fail(
            "No compatible model found for '{}' "
            "(spaCy v{}).".format(model, about.__version__),
            exits=1,
        )
    return comp[model][0]


def download_model(filename, user_pip_args=None):
    download_url = about.__download_url__ + "/" + filename
    pip_args = ["--no-cache-dir", "--no-deps"]
    if user_pip_args:
        pip_args.extend(user_pip_args)
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]
    return subprocess.call(cmd, env=os.environ.copy())
