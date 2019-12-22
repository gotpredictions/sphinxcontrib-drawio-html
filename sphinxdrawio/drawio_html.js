
function bytesToString(arr)
{
    var str = '';

    for (var i = 0; i < arr.length; i++)
    {
        str += String.fromCharCode(arr[i]);
    }

    return str;
};

function getRoot(target) {
    dio_container = $(target)
    while(!dio_container.hasClass('drawio-html-container-div')) 
        dio_container = dio_container.parent()
    return dio_container
}


function showall(icon) {

    dio_container = getRoot(icon)

    if($(icon).hasClass("fa-plus-square-o")) {
        $(icon).removeClass("fa-plus-square-o")
        $(icon).addClass("fa-minus-square-o")

        // hide navigation
        dio_container.find(".drawio-html-navigation").each(function(){$(this).hide()})

        // Show all graphs
        dio_container.find(".drawio-html-graph").each(function(){$(this).show()})

        // show all captions
        dio_container.find(".drawio-html-graph-caption").each(function(){$(this).show()})
    } else {
        $(icon).removeClass("fa-minus-square-o")
        $(icon).addClass("fa-plus-square-o")

        // show navigation
        dio_container.find(".drawio-html-navigation").each(function(){$(this).show()})
        // hide all graphs
        dio_container.find(".drawio-html-graph").each(function(){$(this).hide()})
        // hide all captions
        dio_container.find(".drawio-html-graph-caption").each(function(){$(this).hide()})

        showSlection(dio_container.find(".drawio-html-navigation span")[0])
    }
}

function showSlection(target) {
    dio_container = $(target).parent().parent().parent()
    dio_container.find(".drawio-html-graph").each(function(){
        g = $(this)
        if(g.attr("graph-name") === target.innerText) {
            g.show()
        } else {
            g.hide()
        }
    })

    // Remove current selection
    dio_container.find("span.drawio-current").each(function(){
        $(this).removeClass("drawio-current")
    })

    // Find the span with correct name
    $(target).addClass("drawio-current")
}

function mxClientOnLoad(stylesheet)
{
    var graph = null;
    var xml = null;

    jQuery("mxfile").each(function(){

        count = 0

        // Append the boiler place
        mxfile = $(this)
        $(`<div class="drawio-html-navigation-container">
               <div class="drawio-html-navigation">
               </div>
               <div class="drawio-html-navigation-options">
                   <span class="fa fa-plus-square-o" onclick="showall(event.target)"></span>
               </div>
            </div>
            <div class="drawio-html-graph-container">
            </div>`
        ).insertAfter(mxfile.parent())

        dio_container = mxfile.parent().parent()

        mxfile.find("diagram").each(function(){

            count = count + 1

            diagram = $(this)
            xml = diagram.text();		
            xml = decodeURIComponent(bytesToString(pako.inflateRaw(atob(xml))))
            diagram_name = diagram.attr("name")

            $(dio_container.find(".drawio-html-navigation")[0]).append(
                "<span class='drawio-html-navigation-item' onclick='showSlection(event.target)'>"+diagram_name+"</span>"
            )
            
            var div = document.createElement('div');
            div.className = "drawio-html-graph"
            div.setAttribute("graph-name", diagram_name)
            // div.id = "graph-"+diagram.attr("id")
            $(dio_container.find(".drawio-html-graph-container")[0]).append("<div class='drawio-html-graph-caption'>"+diagram_name+"</div>")
            $(dio_container.find(".drawio-html-graph-container")[0]).append(div)

            graph = new mxGraph(div);
            graph.resetViewOnRootChange = false;
            graph.foldingEnabled = false;
            // NOTE: Tooltips require CSS
            graph.setTooltips(true);
            graph.setEnabled(false);
            graph.setHtmlLabels(true);
            
            // Loads the stylesheet
            if (stylesheet != null)
            {
                var xmlDoc = mxUtils.parseXml(stylesheet);
                var dec = new mxCodec(xmlDoc);
                dec.decode(xmlDoc.documentElement, graph.getStylesheet());
            }
            
            var xmlDoc = mxUtils.parseXml(xml);
            var codec = new mxCodec(xmlDoc);
            codec.decode(codec.document.documentElement, graph.getModel());
            graph.maxFitScale = 1;
            graph.fit();
            graph.center(true, false);
        })

        // hide all captions
        // dio_container.find(".drawio-html-graph-caption").each(function(){$(this).hide()})
        no_navigation = dio_container.attr("drawio-nonav") === "1"
        
        if(count < 2 || no_navigation) {
            // No navigation.  Make everything visible, except navigation
            $(dio_container.find(".drawio-html-navigation-container")[0]).hide()
            
            force_show = dio_container.attr("drawio-show-name") === "1"
            if(count < 2 && !force_show) {
                dio_container.find(".drawio-html-graph-caption").each(function(){$(this).hide()})
            }
        } else {
            // We have navigation 
            show_expanded = dio_container.attr("drawio-expanded") === "1"
            if(show_expanded) {
                // Hide captions
                dio_container.find(".drawio-html-navigation").each(function(){$(this).hide()})

                // Setup right icon
                icon = dio_container.find(".drawio-html-navigation-options span")[0]
                $(icon).removeClass("fa-plus-square-o")
                $(icon).addClass("fa-minus-square-o")
            } else {
                dio_container.find(".drawio-html-graph-caption").each(function(){$(this).hide()})
                showSlection(dio_container.find(".drawio-html-navigation span")[0])
            }
        }

    })
}


jQuery(function () {
    var script = document.createElement('script');
    script.src = "https://www.draw.io/embed.js";
    document.body.appendChild(script)
});
