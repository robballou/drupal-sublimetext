# Drupal Sublime Text

Adds Drupal 7 snippets/functionality. Find the source on Github: https://github.com/robballou/drupal-sublimetext

## Installation

### With Package Control

If you have the [Package Control][package_control] package installed, you can install Drupal from inside Sublime Text itself. Open the Command Palette and select "Package Control: Install Package", then search for Drupal and you're done!

### With Git

#### Mac OS X:

	pushd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone git://github.com/robballou/drupal-sublimetext.git Drupal
    popd

#### Windows 7:

	cd "C:\Users\[your username]\AppData\Roaming\Sublime Text 2\Packages"
	git clone git://github.com/robballou/drupal-sublimetext.git Drupal

## Usage

Most of this package adds snippets for Drupal 7 core functions. I am still working on adding/checking that these functions are created correctly, but most of the functions should be there. There is also some information about [snippets in the Sublime documentation](http://docs.sublimetext.info/en/latest/extensibility/snippets.html).

Snippets can also be accessed via the command palette.

There also are some other completions for constants. There still needs to be a big import for some constants here but for now this should help if you use these in your site development. Recently I added a package I have been using for Drupal module info files which provides syntax highlighting, but also a few snippets and completions.

[package_control]: http://wbond.net/sublime_packages/package_control