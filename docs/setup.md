# Setup

Apologies I shall only cover **Mac** - One day I may include Linux and Windows. And please note that this setup seems far too long! Python is great but surely there is an easier setup. Well... let's do it.

Install [Homebrew](https://brew.sh) for easy package management on Mac:

```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install essentials:

```bash
brew update
brew install python
```

Now **python** is available in the three following ways:

```bash
python
python2
python3
```

We want to use Python 3 (3.7.0 being the latest at this moment in time). Let's manage our Python versions via:

Odd, but we have to make sure Xcode is up to date by doing the following first:

```bash
xcode-select --install
```

```bash
brew install readline xz
brew install zlib
brew install pyenv
```

We can then "install" Python versions to manage. Again I'll just use the latest (though watch out as noted below):

```bash
pyenv install 3.7.0
```

Note that the above may fail if your Mac is running **Mojave**. In that case amend the above command as:

```bash
CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install 3.7.0
```

Now check the available versions:

```bash
pyenv versions
```

And a quick note on why the installation of **readline** and **xz**? Apparently this resolves some Homebrew bug. Go figure!
Also, **zlib** is required by **pyenv**.

We can use our required version of Python be selecting is **globally** or **locally** i.e. per project.

I'll simply go "global":

```bash
pyenv global 3.7.0
```

We want to use [Pip](https://pypi.org/project/pip/) to install third parties, but **Pip** defaults to Python version 2, where we want version 3.
Doing the following should give us what we want:

```bash
python3 get-pip.py
```

To install third party modules, we could do the following, as an example:

```bash
pip install pycrypto
```

If we have not run **python3 get-pip.py** then the above would need to be run as **pip3 install pycrypto**.

But wait! Whoops! We have just installed the pycrypto module globally. What if different projects need different versions?

We can install third modules per project by using the (optional) Python package manager [Anaconda](https://www.anaconda.com/download/#macos).
I don't know! Where on earth do they come up we these names?

We can once again install using Homebrew:

```bash
brew cask install anaconda
```

and then add the following to your profile script such as ~/.zshrc

```vi
export PATH="/usr/local/anaconda3/bin:$PATH"
```

followed by the usual:

```bash
source ~/.zshrc
```

Next we want to install the [Anaconda Navigator](https://anaconda.org/anaconda/anaconda-navigator). Here is the website's description:
> Anaconda Navigator is a desktop graphical user interface included in Anaconda that allows you to launch applications and easily manage conda packages, environments and channels without the need to use command line commands.

The Navigator has a UI - take a look by running:

```bash
anaconda-navigator
```

Note that an alternative approach would be to use [Virtualenv](https://virtualenv.pypa.io).
However, for convenience I've been cheating and simply installing libraries global.