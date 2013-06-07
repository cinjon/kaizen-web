// mapdata:
// {mapping:Mapping,
//  links:
//     [(_id1, x1, y1, _id2, x2, y2, line_weight), ...] // Includes root
//  root: {position:(cx, cy),
//         radius:num_strength,
//         _id:cryptstring},
//  sites:{_id:
//           {position:(cx, cy),
//            radius:num_strength,
//            site:SiteSerialized},
//         ...}
//  notes:{_id:
//           {position:(cx, cy),
//            radius:num_strength,
//            note:NoteSerialized},
//         ...}
// }

var svg, width, height, radius;
var links, notes, sites;

var mapdata, note_banner_html;

//tool to connect nodes. false if off, true if on
var connect_tool_state;
//a node if one has been selected via connect_tool
//after selecting a second node, completes the connection and turns off connect_tool
var connect_tool_node;

function showMappingVisualization(server_data, show, jinja_banner) {
    if (server_data && show) {
        mapdata = server_data;
        note_banner_html = jinja_banner;
        display_root();
        start_map_sandlot();
    }
}

start_map_sandlot = function() {
    set_initial_conditions($("#map-sandlot"));
    svg = d3.select("#map-sandlot")
        .append("svg:svg")
        .style("width", width)
        .style("height", height);

    make_tools();
    make_links(mapdata.links);
    make_root(mapdata.root, mapdata.mapping.name);
    make_sites(mapdata.sites);
    make_notes(mapdata.notes);
};

set_initial_conditions = function(sandlot) {
    set_dimensions = function(sandlot) {
        width = 1050; //width = sandlot.width();
        height = 600;
    };
    set_connect_tool = function() {
        connect_tool_state = false;
        connect_tool_node = null;
    }
    set_objects = function() {
        links = {};
        notes = {};
        sites = {};
    }

    set_dimensions(sandlot);
    set_objects();
    set_connect_tool();
};

is_connect_node = function(node) {
    if (connect_tool_state && connect_tool_node && node.attr("id") == connect_tool_node.attr("id")) {
        return true;
    }
    return false;
}

mouseover = function(node, color) {
    if (!is_connect_node(node)) {
        node.style("fill", color);
    }
}

mouseout = function(node, color) {
    if (!is_connect_node(node)) {
        node.style("fill", color);
    }
}

make_tools = function() {
    _make_connection_tool();
}

_make_connection_tool = function() {
    var x, y, w, h;
    x = 8;
    y = 18;
    w = 90;
    h = 40;
    var tool = svg.append("svg:rect")
        .attr("x", x).attr("y", y)
        .attr("width", w+4).attr("height", h+4)
        .attr("fill", "#dceaf4").attr("id", "connectTool")
        .attr("rx", 7).attr("ry", 7)
        .on("click", connect_tool_click)
        .on("mouseover", function() {d3.select(this).style("fill", "gray");})
        .on("mouseout", function() {d3.select(this).style("fill", "#dceaf4");});
    var text = make_node_text("t" + tool.attr("id"), "Connect Off", x+2, y+h/2+5, connect_tool_click, "blue");
}

connect_tool_click = function() {
    connect_tool_state = !connect_tool_state
    console.log(connect_tool_state);
    if (connect_tool_state) {
        $("#tconnectTool").text("Connect On");
    } else {
        $("#tconnectTool").text("Connect Off");
        clean_connect_selection();
    }
}

clean_connect_selection = function() {
    connect_tool_node = null;
}

display_root = function() {
    $("#map-root")[0].innerHTML = _display_root_name();
    $("#map-site").hide();
    $("#map-note").hide();
    $("#map-root").show();
}

_display_root_name = function() {
    return '<p style="margin-top:20px; font-size:30px; text-align:center;">' + mapdata.mapping.mapname + '</p>';
}

display_note = function(_id) {
    data = mapdata.notes[_id];
    $("#map-note")[0].innerHTML = note_banner_html[0] + data.note + note_banner_html[1];
    $("#map-site").hide();
    $("#map-root").hide();
    $("#map-note").show();
}

display_site = function(_id) {
    data = mapdata.sites[_id];
    $("#site-title")[0].innerHTML = '<p><a href="' + data.site.url + '">' + data.site.title + '</a></p>';
    $("#map-note").hide();
    $("#map-root").hide();
    $("#map-site").show();
}

drag = function(move) {
    return d3.behavior.drag().on("drag", move);
}

move_links = function(node) {
    nodelinks = links[node.attr("id")];
    for (var index in nodelinks) {
        var link = $("#" + nodelinks[index][0]);
        var end  = nodelinks[index][1];
        link.attr("x" + end, node.attr("link_x"))
            .attr("y" + end, node.attr("link_y"));
    }
}

move_site = function() {
    var circle = d3.select(this);
    var text = $("#t" + circle.attr("id"));
    var r  = parseInt(circle.attr("r"));
    var box_width =  Math.max(text[0].getBBox().width, 2*r);

    var cx = parseInt(circle.attr("cx"));
    var cy = parseInt(circle.attr("cy"));
    var new_cx = Math.max(r, Math.min(width - box_width + r, d3.event.dx + cx));
    var new_cy = Math.max(r, Math.min(height - r, d3.event.dy + cy));

    circle.attr("cx", new_cx).attr("cy", new_cy);
    circle.attr("link_x", new_cx).attr("link_y", new_cy);
    text.attr("x", new_cx - r).attr("y", new_cy);
    move_links(circle);
};

move_note = function() {
    var rect = d3.select(this);
    var text = $("#t" + rect.attr("id"));
    var d = parseInt(rect.attr("width"));
    var box_width = Math.max(text[0].getBBox().width, d);
    var box_height = Math.max(text[0].getBBox().height, d);

    var x = parseInt(rect.attr("x"));
    var y = parseInt(rect.attr("y"));
    var new_x = Math.max(d, Math.min(width - box_width + d, d3.event.dx + x));
    var new_y = Math.max(d, Math.min(height - box_height, d3.event.dy + y));

    rect.attr("x", new_x).attr("y", new_y);
    rect.attr("link_x", new_x + d/2).attr("link_y", new_y + d/2);
    text.attr("x", new_x).attr("y", new_y + d/2);
    move_links(rect);
}

make_root = function(maproot, name) {
    var circle, text, click_func;
    click_func = function() {return display_root();};
    circle = svg.append("svg:circle")
        .attr("class", "rootNode")
        .attr("id", maproot._id)
        .attr("cx", maproot.position[0])
        .attr("cy", maproot.position[1])
        .attr("r", maproot.radius)
        .attr("fill", "wheat")
        .attr("stroke", "#dceaf4")
        .on("click", click_func)
        .on("mouseover", function() {mouseover(d3.select(this), "gray");})
        .on("mouseout", function() {mouseout(d3.select(this), "wheat");})
        .call(drag(move_site));
    text = make_node_text("t" + maproot._id, name, maproot.position[0]-maproot.radius, maproot.position[1], click_func);
}

make_sites = function(mapsites) {
    for (var key in mapsites) {
        //replace name (second key) with some name
        make_site(key, key, mapsites[key].position, mapsites[key].radius);
        sites[key] = mapsites[key].site;
    }
}

make_site = function(_id, name, position, radius) {
    var circle, text, click_func;
    click_func = function() {return click(connect_node, display_site, _id);};
    circle = svg.append("svg:circle")
        .attr("class", "siteNode")
        .attr("id", _id)
        .attr("r", radius)
        .attr("cx", position[0])
        .attr("cy", position[1])
        .attr("link_x", position[0])
        .attr("link_y", position[1])
        .attr("fill", "#0772A1")
        .on("click", click_func)
        .on("mouseover", function() {mouseover(d3.select(this), "gray");})
        .on("mouseout", function() {mouseout(d3.select(this), "#0772A1");})
        .call(drag(move_site));
    text = make_node_text("t" + _id, name, position[0]-radius, position[1], click_func);
}

make_notes = function(mapnotes) {
    for (var key in mapnotes) {
        make_note(key, key, mapnotes[key].position, mapnotes[key].radius);
        notes[key] = mapnotes[key].note;
    }
}

make_note = function(_id, name, position, radius) {
    var side = 30;
    var click_func = function() {return click(connect_node, display_note, _id);};
    var rect = svg.append("svg:rect")
        .attr("class", "noteNode")
        .attr("id", _id)
        .attr("x", position[0] - side/2)
        .attr("y", position[1] - side/2)
        .attr("link_x", position[0] - side/2)
        .attr("link_y", position[1] - side/2)
        .attr("width", side)
        .attr("height", side)
        .attr("fill", "rgb(6,120,155)") //#FF7340
        .attr("rx", 7)
        .attr("ry", 7)
        .attr("stroke-width", 5)
        .attr("opacity", .6)
        .on("click", click_func)
        .on("mouseover", function() {mouseover(d3.select(this), "gray");})
        .on("mouseout", function() {mouseout(d3.select(this), "rgb(6,120,155)");})
        .call(drag(move_note));
    var text = make_node_text("t" + _id, name, position[0] - side/2, position[1], click_func);

}

make_node_text = function(_id, name, x, y, click_func, color) {
    if (!color) {
        color = "red";
    }
    var text = svg.append("svg:text")
        .attr("x", x)
        .attr("y", y)
        .text(name)
        .attr("id", _id)
        .attr("font-family", "helvetica")
        .attr("font-size", "16px")
        .attr("fill", color)
        .attr("class", "textNode");
    if (click_func) {
        text.on("click", click_func);
    }
    return text;
};

click = function(_do_connect, _do_click, _id) {
    if (connect_tool_state && _do_connect) {
        return _do_connect(_id);
    }
    else if (_do_click) {
        return _do_click(_id);
    }
    return;
}

//When unique str id, make just one connect func
connect_node = function(_id) {
    var node = $("#" + _id);
    if (connect_tool_node == null) {
        node.attr("fill", "#FF7340");
        connect_tool_node = node;
        console.log('set connect_tool_ndoe to node');
        console.log(connect_tool_node);
        console.log(node.attr("id"));
    } else {
        make_link(connect_tool_node.attr("link_x"), connect_tool_node.attr("link_y"),
                  node.attr("link_x"), node.attr("link_y"),
                  connect_tool_node.attr("id"), node.attr("id"));
    }
}

make_links = function(maplinks) {
    console.log('in makelinks');
    console.log(maplinks);
    for (var index in maplinks) {
        var maplink = maplinks[index];
        var _id1 = maplink[0];
        var _id2 = maplink[3];
        var link = make_link(maplink[1], maplink[2],
                             maplink[4], maplink[5],
                             _id1, _id2, maplink[6]);
        add_link_to_links(link, _id1, _id2);
    }
}

make_link = function(e1x, e1y, e2x, e2y, e1id, e2id, weight) {
    //TODO utilize weight
    var link = svg.append("svg:line")
        .attr("x1", e1x)
        .attr("y1", e1y)
        .attr("x2", e2x)
        .attr("y2", e2y)
        .attr("class", "link")
        .attr("id", e1id + '_' + e2id)
        .style("stroke", "#3E97D1")
        .style("stroke-width", 5)
        .style("stroke-opacity", .3)
    return link;
}

add_link_to_links = function(link, id1, id2) {
    if (!(id1 in links)) {
        links[id1] = [];
    }
    if (!(id2 in links)) {
        links[id2] = [];
    }
    //can i push the object instead? how do i access it afterward...
    links[id1].push([link.attr("id"), '1']);
    links[id2].push([link.attr("id"), '2']);
}


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
