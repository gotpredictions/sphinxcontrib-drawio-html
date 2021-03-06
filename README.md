# sphinxcontrib-drawio-html
Sphinx Extension to add the ``drawio-html`` directive to include 
draw.io diagrams into the generated HTML documentation.

**Important:** This is an alpha extension and as such may not work or
fit your needs 100%.  See the KNOWN ISSUES SECTION. 

## Installation

1. ``python3 -m pip install sphinxcontrib-drawio-html`` or use ``pipenv`` 
2. In your sphinx config:
```python
extensions = [
    "sphinxdrawio.drawio_html"
]
```

## Options

At this time no options in ``conf.py`` are supported. 

## Usage
```
.. drawio-html:: example.drawio
    :page: class-diagram
    :expanded:
    :hide-nav:
    :force-name:

    style-overrides

```

## known issues
1. This extension is tested using read-the-docs theme only.  It uses jQuery and font-awesome
   that comes with rtd theme, and without the theme, it will not likely work. 
2. Only HTML translators are created, which means Latex and PDF support will not likely
   work. PDF and other builders are not tried at all. 
3. Custom styleoverrides are working intermittently.  Some with HTML/CSS expertise might
   help in troubleshooting why not. 

## Wish list 
1. Provide defaults in the conf.py for expanded, hide-nav and force-name so that, a site
   can decide their basic way of showing the files.  Currently it has to be done at 
   each file. 
2. Change the content area to accept some rst per page in the draw.io diagram so that it
   can interspread easily with in the diagrams.  Presentation can also be changed to show
   the diagrams and content for that section. Only option for now is the add multiple
   directives. 
    ```
    .. drawio-html:: example.drawio
        :expanded:
        :hide-nav:
        :force-name:

        style-overrides

        class-diagram:
            lorum ipsum dorum

        sequence-diagram:
            nice orderly work.

    ```
3. Add some tests.  Do not even know how other sphinx extensions are tested. 
4. Full screen display of the diagrams. 
5. Provided notes can be added per diagram, provide a layout option to place
   notes on the right or bottom. 

Do file issues if you see something, or better yet open a pull request :-) 

## ACKNOWLEDGEMENTS

1. This is inspired by the work done earlier here:  https://github.com/Modelmat/sphinxcontrib-drawio
2. HTML/CSS expertise is generously provided by https://github.com/BabyManisha
