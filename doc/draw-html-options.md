## Options for customizing. 

### Page
Specify the pages to be rendered.  This option is encorced in 
python part of the extension.  Only the content for the diagrams 
of the specified pages is embedded into the HTML generation. 

### expanded
When this flag is selected, we start off in the expanded mode.  
Minimize is still available.  When there is only page, expand/collapse
along with page name is automatically hidden. 

### hide-nav
Hide the navigation completely.  This will automatically enable
expansion and displays all the pages. 

### force-name
When there is only one page, navigation is hidden the page name
is not displayed with the assumption that the context around the
diagram is generally enough.  However the name display can be
enabled by chosing the force-name. 

## Content of the directive. 

Content of the directive is treated as CSS styles.  Each diagram is
given a unique id, and `div#id` is prefixed to each line automatically
so that the styling is scoped to the given id.  _NOTE: No CSS parser is used
and we assume each line to be a complete CSS directive_.  This option is 
working intermittently for some reason.  
  