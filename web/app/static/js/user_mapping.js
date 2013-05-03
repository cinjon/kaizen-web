var width, height, radius, linklength, groups;

function showMappingVisualization(mapdata, show) {
    if (mapdata && show) {
        $('#mapName').html('<p><b>' + mapdata.mapname + '</b></p>');
        start_map_nav();
        start_map_sandlot(mapdata);
        start_map_sites(mapdata);
        start_map_notes(mapdata);
    } else {
        console.log('no notes, yo');
    }
}

start_map_nav = function() {
    //map navigation, e.g. "add", "delete", "connect"
}

start_map_sandlot = function(mapdata) {
    set_initial_conditions($("#map-sandlot"));
    var svg = d3.select("#map-sandlot")
        .append("svg:svg")
        .style("width", width)
        .style("height", height);

    if ("start_state" in mapdata) {
        //Do start_state stuff ...
    } else {
        start_map_sandlot_from_blank(mapdata, svg);
    }
};

start_map_sites = function(mapdata) {
    console.log(' in start map sites');
    console.log(mapdata);
    var div_id, site_count, node_r, div_width, div_height, _i;
    div_id = '#map-sites';
    div_width = $(div_id).width();
    div_height = $(div_id).height();
    site_count = mapdata.sites.length;
    node_r = Math.min(div_height/2 - 10, div_width / site_count - 10);
    var svg = d3.select(div_id)
        .append("svg:svg")
        .style("width", div_width)
        .style("height", div_height);

    for (_i = 0; _i < site_count; _i++) {
        var g = svg.append("svg:g");
        var node = g.append("svg:circle")
            .attr("r", node_r)
            .attr("cx", node_r*(2*_i + 1) + 10*(_i + 1))
            .attr("cy", div_height / 2)
            .attr("fill", "#dceaf4");
        var text = make_node_text(g, "testing", node);
    }
}

start_map_notes = function(mapdata) {
    //TODO
}

set_initial_conditions = function(sandlot) {
    set_dimensions = function(sandlot) {
        width = sandlot.width();
        height = 500;
    };
    set_default_radius = function() {
        radius = Math.max(30, Math.min(Math.sqrt(width), Math.sqrt(height)))
    };
    set_default_linklength = function() {
        linklength = 3 * radius;
    };
    set_groups = function() {
        groups = {}; //Keyed by node_id
    };

    set_dimensions(sandlot);
    set_default_radius();
    set_default_linklength();
    set_groups();
};

start_map_sandlot_from_blank = function(mapdata, svg) {
    var rootG = make_node(svg, "root", mapdata.mapname);
//     add_links_to_node(rootG, 5, svg);
};

var drag = d3.behavior.drag().on("drag", move);
function move() {
    var circle = d3.select(this);
    var group = groups[this.parentNode.id];
    var text = group.select('text');

    var cx = parseInt(circle.attr("cx"));
    var cy = parseInt(circle.attr("cy"));
    var r  = parseInt(circle.attr("r"));
    var box_width =  Math.max(text.node().getBBox().width, 2*r);
    var new_cx = Math.max(r, Math.min(width - box_width + r, d3.event.dx + cx));
    var new_cy = Math.max(r, Math.min(height - r, d3.event.dy + cy));
    circle
        .attr("cx", new_cx)
        .attr("cy", new_cy);
    text
        .attr("x", new_cx - circle.attr("r"))
        .attr("y", new_cy);
};

make_node = function(svg, node_id, name) {
    var circle, text, g;
    g = svg.append("svg:g")
        .attr("id", "g_" + node_id);
    groups['g_' + node_id] = g
    if (node_id == "root") {
        circle = g.append("svg:circle")
            .attr("class", "node")
            .attr("cx", width / 2)
            .attr("cy", height / 2)
            .attr("r", radius)
            .attr("fill", "wheat")
            .attr("stroke", "#dceaf4")
            .call(drag);
    } else {

    }

    text = make_node_text(g, name, circle);
    return g;
}

make_node_text = function(g, name, node) {
    return g.append("text")
        .attr("x", node.attr("cx") - node.attr("r"))
        .attr("y", node.attr("cy"))
        .text(name)
        .attr("font-family", "helvetica")
        .attr("font-size", "16px")
        .attr("fill", "red")
        .attr("class", "nodeText");
};

add_links_to_node = function(node, number, svg) {
    var angle, node_x1, node_y1, node_r;
    angle = 2 * Math.PI / number;
    node_r = parseInt(node.attr("r"));
    for (var _i = 0; _i < number; _i++) {
        var x1, y1, x2, y2, rim_angle;
        rim_angle = angle*_i;
        x1 = parseInt(node.attr("cx")) + Math.cos(rim_angle) * node_r;
        y1 = parseInt(node.attr("cy")) + Math.sin(rim_angle) * node_r;
        x2 = x1 + Math.cos(rim_angle) * linklength;
        y2 = y1 + Math.sin(rim_angle) * linklength;
        var link = svg.append("svg:line")
            .attr("x1", x1)
            .attr("y1", y1)
            .attr("x2", x2)
            .attr("y2", y2)
            .attr("class", "link")
            .attr("class", node.attr("id"))
            .style("stroke", "#CCC");
    }
};

start_sidebar_with_notes = function(url_notes, mapping, sidebar_id) {
    var sidebar = document.getElementById(sidebar_id);
    for (var i = 0; i < url_notes.length; i++) {
        var url = url_notes[i];
        var title = document.createElement('div');
        title.class = 'row-fluid';
        title.innerHTML = '<a href="' + url.url + '"><p>' + url.title + '</p></a>';
        sidebar.appendChild(title);

        for (var j = 0; j < url.notes.length; j++) {
            var rowfluid = document.createElement('div');
            rowfluid.class = 'row-fluid';
            var spanOne = document.createElement('div');
            spanOne.class = 'span1';
            var spanTen = document.createElement('div');
            spanTen.class = 'span10 offset1';
            rowfluid.appendChild(spanOne);
            rowfluid.appendChild(spanTen);
            title.appendChild(rowfluid);

            var note = url.notes[j];
            var date = new Date(note.time * 1000);
//             var textBox = fitString(null, note.text, 50);
            var text = note.text;
            spanOne.innerHTML = '<p>' + date.getMonth() + '/' + date.getDate() + '/' + date.getFullYear() + '</p>';
            spanTen.innerHTML = '<p>' + text + '</p>';
        }
    }
};

// fitString = function(ctx, str, widthMax) {
//     var textBlock = [];
//     var words = str.split(" ");
//     var position = 0;
//     while (position < words.length) {
//         var sentence = words[position];
//         position += 1;
//         while (position < words.length && checkStrLength(ctx, sentence, words[position], widthMax)) {
//             sentence += " ";
//             sentence += words[position];
//             position += 1;
//         }
//         textBlock.push(sentence);
//     }
//     return textBlock;
// };

// checkStrLength = function(ctx, str, word, max) {
//     if (ctx) {return (ctx.measureText(str + word).width + 1 <= max)}
//     else {return ((str + word).length + 1 <= max)}
// };
