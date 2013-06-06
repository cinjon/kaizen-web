//TODO(Cinjon): Change the {note, site}_id_{name} to {note, site}_id_{crypto string}
//We want these strings to be small, say six chars in length, and unique on a page.
//Current system does not do that and is going to create some really bad interactions

// mapdata:
// {mapping:Mapping,
//  site_links:
//     {(site_id_i + '   ' + site_id_j):num_strength,...} //Includes root
//  note_links:
//     {(site_id_i + '   ' + note_id_j):num_strength,...} //Includes root
//  site_id_root:
//     {position:(cx, cy),
//      radius:num_strength}
//  site_id_{name}:
//     {position:(cx, cy),
//      radius:num_strength,
//      site:Site}
//  ...
//  note_id_{name}:
//     {position:(cx, cy),
//      radius:num_strength,
//      note:Note}
//  ...
// }

var svg, width, height, radius;
var links, notes, sites;

var mapdata, mapname, note_banner_html;

//tool to connect nodes. false if off, true if on
var connect_tool_state;
//a node if one has been selected via connect_tool
//after selecting a second node, completes the connection and turns off connect_tool
var connect_tool_node;

function showMappingVisualization(server_data, show, jinja_banner) {
    if (server_data && show) {
        mapdata = server_data;
        mapname = server_data.mapping.name;
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

    //can fix this with the ordering being: make lines, make circles, make rects
    //lines go into links and have the _id's as ends, circles go into sites by _id, rects go into notes by _id
    for (var key in mapdata) {
        if (key == 'site_links' || key == 'note_links' || key.slice(0, 8) == 'note_id_') {
            continue;
        }

        position = mapdata[key]['position']
        radius = mapdata[key]['radius']
        if (key == 'root') {
            //change _id to be the crypto string
            make_root(mapname, mapname, position, radius);
        } else if (key.slice(0, 4) == 'site') {
            //change _id to be the crypto string
            make_site(key.slice(8), key.slice(8), position, radius);
        }
    }

    //We want sites to exist before notes so that we can group them together.
    for (var key in mapdata) {
        if (key.slice(0,8) == 'note_id_') {
            //change_id to be the crypto string
            make_note(key.slice(8), key.slice(8), mapdata[key]['position'],
                      mapdata[key]['radius'], mapdata[key]['note'].sid);
        } else {
            continue
        }
    }

    make_site_site_links(mapdata.site_links);
    make_site_note_links(mapdata.note_links);
};

set_initial_conditions = function(sandlot) {
    set_dimensions = function(sandlot) {
        width = 1050; //width = sandlot.width();
        height = 600;
    };
    set_bools = function() {
        connect_tool_state = false;
    }
    set_links = function() {
        links = {}; //{g_id_i:[(g_id_j, c1), (g_id_k, c2),...] --> c1/c2 is whether it's first or second set of coords
    }

    set_dimensions(sandlot);
    set_links();
};

make_tools = function() {
    _make_connection_tool();
}

_make_connection_tool = function() {
    var x, y, w, h;
    x = 8;
    y = 18;
    w = 62;
    h = 21;
    var tool = svg.append("svg:rect")
        .attr("x", x).attr("y", y)
        .attr("width", w+4).attr("height", h+4)
        .attr("fill", "#dceaf4").attr("id", "connectTool")
        .attr("rx", 7).attr("ry", 7)
        .on("click", connect_tool_click);
    var text = make_node_text("connectTool", "Connect", x+2, y+h/2+5, "connectTool", connect_tool_click, "blue");
}

connect_tool_click = function() {
    connect_tool_state = !connect_tool_state
    if (!connect_tool_state) {
        clean_connect_selection();
    }
}

clean_connect_selection = function() {
    connect_tool_node = null;
}

display_root = function() {
    $("#map-root")[0].innerHTML = _display_root_name(mapname);
    $("#map-site").hide();
    $("#map-note").hide();
    $("#map-root").show();
}

_display_root_name = function(mapname) {
    return '<p style="margin-top:20px; font-size:30px; text-align:center;">' + mapname + '</p>';
}

display_note = function(_id) {
    data = mapdata['note_id_' + _id];
    $("#map-note")[0].innerHTML = note_banner_html[0] + data.note + note_banner_html[1];
    $("#map-site").hide();
    $("#map-root").hide();
    $("#map-note").show();
}

display_site = function(_id) {
    data = mapdata['site_id_' + _id];
    $("#site-title")[0].innerHTML = '<p><a href="' + data.site.url + '">' + data.site.title + '</a></p>';
    $("#map-note").hide();
    $("#map-root").hide();
    $("#map-site").show();
}

drag = function(move) {
    return d3.behavior.drag().on("drag", move);
}

function move_site() {
    var circle = d3.select(this);
    console.log(circle.attr("id"));
    var text = $("#t" + circle.attr("id").slice(1));
    var r  = parseInt(circle.attr("r"));
    var box_width =  Math.max(text[0].getBBox().width, 2*r);

    var cx = parseInt(circle.attr("cx"));
    var cy = parseInt(circle.attr("cy"));
    var new_cx = Math.max(r, Math.min(width - box_width + r, d3.event.dx + cx));
    var new_cy = Math.max(r, Math.min(height - r, d3.event.dy + cy));

    circle.attr("cx", new_cx).attr("cy", new_cy);
    text.attr("x", new_cx - r).attr("y", new_cy);
};

function move_note() {
    var rect = d3.select(this);
    var text = $("#t" + rect.attr("id").slice(1));
    var d = parseInt(rect.attr("width"));
    var box_width = Math.max(text[0].getBBox().width, d);
    var box_height = Math.max(text[0].getBBox().height, d);

    var x = parseInt(rect.attr("x"));
    var y = parseInt(rect.attr("y"));
    var new_x = Math.max(d, Math.min(width - box_width + d, d3.event.dx + x));
    var new_y = Math.max(d, Math.min(height - box_height, d3.event.dy + y));

    rect.attr("x", new_x).attr("y", new_y);
    text.attr("x", new_x).attr("y", new_y + d/2);
}

make_root = function(_id, name, position, radius) {
    var circle, text, click_func;
    click_func = function() {display_root();};
    circle = svg.append("svg:circle")
        .attr("class", "rootNode")
        .attr("id", "r" + _id)
        .attr("cx", position[0])
        .attr("cy", position[1])
        .attr("r", radius)
        .attr("fill", "wheat")
        .attr("stroke", "#dceaf4")
        .on("click", click_func)
        .on("mouseover", function(){d3.select(this).style("fill", "aliceblue");})
        .on("mouseout", function(){d3.select(this).style("fill", "wheat");})
        .call(drag(move_site));
    text = make_node_text("t" + _id, name, position[0]-radius, position[1], 'rootText', click_func);
}

make_site = function(_id, name, position, radius) {
    var circle, text, click_func;
    click_func = click(connect_site, display_site, _id);
    circle = svg.append("svg:circle")
        .attr("class", "siteNode")
        .attr("id", "s" + _id)
        .attr("r", radius)
        .attr("cx", position[0])
        .attr("cy", position[1])
        .attr("fill", "#dceaf4")
        .on("click", click_func)
        .on("mouseover", function(){d3.select(this).style("fill", "aliceblue");})
        .on("mouseout", function(){d3.select(this).style("fill", "#dceaf4");})
        .call(drag(move_site));
    text = make_node_text("t" + _id, name, position[0]-radius, position[1], click_func);
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
connect_note = function(_id) {
    var note_node = $("#n" + _id);
    if (connect_tool_node == null) {
        connect_tool_node = note_node;
    } else if (connect_tool_node.attr("id").slice(1, 2) == "n") {
        //already exists a note node, connect this one to that one
        make_note_note_link(connect_tool_node, note_node, null);
    } else if (connect_tool_node.attr("id").slice(1, 2) == "s") {
        make_site_note_link(connect_tool_node, note_node, null);
    }
}

connect_site = function(_id) {
    var site_node = $("#s" + _id);
    if (connect_tool_node == null) {
        connect_tool_node = site_node;
    } else if (connect_tool_node.attr("id").slice(1, 2) == "n") {
        //already exists a note node, connect this one to that one
        make_site_note_link(site_node, connect_tool_node, null);
    } else if (connect_tool_node.attr("id").slice(1, 2) == "s") {
        make_site_site_link(connect_tool_node, note_node, null);
    }
}

make_note = function(_id, name, position, radius, site) {
    var side = 30;
    var click_func = click(connect_note, display_note, _id)
    var rect = svg.append("svg:rect")
        .attr("class", "noteNode")
        .attr("id", "n" + _id)
        .attr("x", position[0] - side/2)
        .attr("y", position[1] - side/2)
        .attr("width", side)
        .attr("height", side)
        .attr("fill", "#FF7340")
        .attr("rx", 7)
        .attr("ry", 7)
        .attr("stroke-width", 5)
        .attr("opacity", .5)
        .on("click", click_func)
        .on("mouseover", function(){d3.select(this).style("fill", "aliceblue");})
        .on("mouseout", function(){d3.select(this).style("fill", "#FF7340");})
        .call(drag(move_note));
    var text = make_node_text("t" + _id, name, position[0] - side/2, position[1], 'noteText', click_func);
}

make_site_site_links = function(site_links) {
    for (var key in site_links) {
        var line_weight = site_links[key];
        var link_pair = key.split('   ');
        var id1 = link_pair[0].slice(8);
        var id2 = link_pair[1].slice(8);
        var c1 = $("#s" + id1);
        var c2 = $("#s" + id2);
        make_site_site_link(c1, c2, line_weight);
    }
}

make_site_site_link = function(c1, c2, weight, ends) {
    var link = make_link(parseInt(c1.attr("cx")), parseInt(c1.attr("cy")),
                         parseInt(c2.attr("cx")), parseInt(c2.attr("cy")),
                         weight, c1.attr("id"), c2.attr("id"))
    add_link_to_links(link, c1, c2);
}

make_site_note_links = function(note_links) {
    for (var key in note_links) {
        var line_weight = note_links[key];
        var link_pair = key.split('   ');
        var sid = link_pair[0].slice(8);
        var nid = link_pair[1].slice(8);
        var c = $("#s" + sid);
        var r = $("#n" + nid);
        make_site_note_link(c, r, line_weight)
    }
}

make_site_note_link = function(c, r, weight) {
    var link = make_link(parseInt(c.attr("cx")), parseInt(c.attr("cy")),
                         parseInt(r.attr("x")) + parseInt(r.attr("width"))/2,
                         parseInt(r.attr("y")) + parseInt(r.attr("height"))/2,
                         weight, c.attr("id"), r.attr("id"));
    add_link_to_links(link, c, r);
}

make_note_note_link = function(r1, r2, weight) {
    var link = make_link(parseInt(r1.attr("x")) + parseInt(r1.attr("width"))/2,
                         parseInt(r1.attr("y")) + parseInt(r1.attr("height"))/2,
                         parseInt(r2.attr("x")) + parseInt(r2.attr("width"))/2,
                         parseInt(r2.attr("y")) + parseInt(r2.attr("height"))/2,
                         weight, c.attr("id"), r.attr("id"));
    add_link_to_links(link, r1, r2);
}

make_link = function(e1x, e1y, e2x, e2y, weight, e1id, e2id) {
    //TODO utilize weight
    var link = svg.append("svg:line")
        .attr("x1", e1x)
        .attr("y1", e1y)
        .attr("x2", e2x)
        .attr("y2", e2y)
        .attr("class", "note_link")
        .attr("id", e1id + '_' + e2id)
        .style("stroke", "#CCC");
    return link;
}

add_link_to_links = function(link, e1, e2) {
    id1 = e1.attr("id");
    id2 = e2.attr("id");
    if (!(id1 in links)) {
        links[id1] = [];
    }
    if (!(id2 in links)) {
        links[id2] = [];
    }

    links[id1].push((link, '1'));
    links[id2].push((link, '2'));
}

// reorder_edges_below = function(svg) {
//     gs = svg.selectAll("g");
//     for (var g in gs) {
//         ;


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
