// mapdata:
// {mapname:name,
//  site_links:
//     {(site_id_i + '   ' + site_id_j):num_strength,...} //Includes root
//  note_links:
//     {(site_id_i + '   ' + note_id_j):num_strength,...} //Includes root
//  site_id_root:
//     {position:(cx, cy),
//      radius:num_strength}
//  site_id_0:
//     {position:(cx, cy),
//      radius:num_strength,
//      url:url,
//      title:title}
//  ...
//  note_id_0:
//     {position:(cx, cy),
//      radius:num_strength,
//      text:text,
//      time:#,
//      site:{0, 1, ...}}
//  ...
// }


var width, height, radius;
var links, groups, rects;
var mapdata;
//Groups are a draggable selection, e.g. a node along with its txt and notes
//Links are a deletable line. When dragging a group, should drag the link with it
//Rects is a dict of note_id to rectangle.

function showMappingVisualization(server_data, show) {
    if (server_data && show) {
        mapdata = server_data;
        start_map_sandlot();
    }
}

start_map_sandlot = function() {
    set_initial_conditions($("#map-sandlot"));
    var svg = d3.select("#map-sandlot")
        .append("svg:svg")
        .style("width", width)
        .style("height", height);

    for (var key in mapdata) {
        if (key == 'site_links' || key == 'note_links' || key.slice(0, 8) == 'note_id_') {
            continue;
        }

        position = mapdata[key]['position']
        radius = mapdata[key]['radius']
        if (key == 'root') {
            make_root(svg, mapdata.mapname, position, radius);
        } else if (key.slice(0, 4) == 'site') {
            make_site(svg, key.slice(8), position, radius);
        }
    }

    //We want sites to exist before notes so that we can group them together.
    for (var key in mapdata) {
        if (key.slice(0,8) == 'note_id_') {
            make_note(svg, key.slice(8), mapdata[key]['position'],
                      mapdata[key]['radius'], mapdata[key]['site']);
        } else {
            continue
        }
    }

    make_site_links(svg, mapdata.site_links);
    make_note_links(svg, mapdata.note_links);
};

set_initial_conditions = function(sandlot) {
    set_dimensions = function(sandlot) {
        width = 1050; //width = sandlot.width();

        height = 600;
    };
    set_groups = function() {
        groups = {}; //Keyed by node_id
    };
    set_links = function() {
        links = {}; //{g_id_i:[(g_id_j, c1), (g_id_k, c2),...] --> c1/c2 is whether it's first or second set of coords
    }
    set_rects = function() {
        rects = {};
    }

    set_dimensions(sandlot);
    set_groups();
    set_links();
    set_rects();
};

function display_note(name) {
    data = mapdata['note_id_' + name];
    var date = new Date(data.time * 1000);
    $("#note-time")[0].innerHTML = '<p>' + date.getMonth() + '/' + date.getDate() + '/' + date.getFullYear() + '</p>';
    $("#note-text")[0].innerHTML = '<p>' + data.text + '</p>';
}

var drag = d3.behavior.drag().on("drag", move);
function move() {
    var circle = d3.select(this);
    var g = $("#" + this.parentNode.id)[0];
    var texts = g.getElementsByTagName('text');
    var rectangles = g.getElementsByTagName('rect');

    var cx = parseInt(circle.attr("cx"));
    var cy = parseInt(circle.attr("cy"));
    var r  = parseInt(circle.attr("r"));
    var box_width =  Math.max(g.getElementsByClassName('siteText')[0].getBBox().width, 2*r);
    var new_cx = Math.max(r, Math.min(width - box_width + r, d3.event.dx + cx));
    var new_cy = Math.max(r, Math.min(height - r, d3.event.dy + cy));

    circle
        .attr("cx", new_cx)
        .attr("cy", new_cy);

//     texts.each(function(text) {
//         console.log('text: ' + text);
//         var new_x = text.attr("x") - (new_cx - cx);
//         var new_y = text.attr("y") - (new_cy - cy);
//         text
//             .attr("x", new_x)
//             .attr("y", new_y);
//     });
    for (var rect in rectangles) {
        var new_x = rect.attr("x") - (new_cx - cx);
        var new_y = rect.attr("y") - (new_cy - cy);
        rect
            .attr("x", new_x)
            .attr("y", new_y);
    }
};

make_root = function(svg, name, position, radius) {
    var circle, text, g, _id;
    _id = 'g_site_root';
    g = svg.append("svg:g")
        .attr("id", _id);
    groups[_id] = g
    circle = g.append("svg:circle")
        .attr("class", "node")
        .attr("cx", position[0])
        .attr("cy", position[1])
        .attr("r", radius)
        .attr("fill", "wheat")
        .attr("stroke", "#dceaf4")
        .call(drag);
    text = make_node_text(g, name, position[0] - radius, position[1], 'rootText');
}

make_site = function(svg, name, position, radius) {
    var circle, text, g, _id;
    _id = 'g_site_' + name;
    g = svg.append("svg:g")
        .attr("id", _id);
    groups[_id] = g;
    circle = g.append("svg:circle")
        .attr("class", "node")
        .attr("r", radius)
        .attr("cx", position[0])
        .attr("cy", position[1])
        .attr("fill", "#dceaf4")
        .call(drag);
    text = make_node_text(g, name, position[0] - radius, position[1], 'siteText');
}

make_node_text = function(g, name, x, y, text_class) {
    return g.append("text")
        .attr("x", x)
        .attr("y", y)
        .text(name)
        .attr("font-family", "helvetica")
        .attr("font-size", "16px")
        .attr("fill", "red")
        .attr("class", text_class);
};

make_note = function(svg, name, position, radius, site) {
    var rectangle, side;
    var g = groups['g_site_' + site];
    groups['g_note_' + name] = g;

    side = 30;
    rectangle = g.append("svg:rect")
        .attr("class", "note")
        .attr("x", position[0] - side/2)
        .attr("y", position[1] - side/2)
        .attr("width", side)
        .attr("height", side)
        .attr("fill", "#FF7340")
        .attr("rx", 7)
        .attr("ry", 7)
        .attr("stroke-width", 5)
        .attr("opacity", .5)
        .attr("id", name)
        .on("click", function() {
            display_note(name);});
    make_node_text(g, name, position[0] - side/2, position[1], 'noteText');
    rects['r_note_' + name] = rectangle;
}

make_site_links = function(svg, site_links) {
    for (var key in site_links) {
        var line_weight = site_links[key];
        var link_pair = key.split('   ');
        var id1 = link_pair[0].slice(8);
        var id2 = link_pair[1].slice(8);
        var g1 = groups['g_site_' + id1];
        var g2 = groups['g_site_' + id2];
        var link = make_site_link(svg, g1.select('circle'), g2.select('circle'),
                                  line_weight, 'groups_s_' + id1 + '_s_' + id2);
        add_link_to_links(link, g1, g2);
    }
}

make_site_link = function(svg, c1, c2, weight, end_ids) {
    //TODO: utilize weight
    var link = svg.append("svg:line")
        .attr("x1", c1.attr("cx"))
        .attr("y1", c1.attr("cy"))
        .attr("x2", c2.attr("cx"))
        .attr("y2", c2.attr("cy"))
        .attr("class", "site_link")
        .attr("id", end_ids)
        .style("stroke", "#CCC");
    return link;
}

make_note_links = function(svg, note_links) {
    for (var key in note_links) {
        var line_weight = note_links[key];
        var link_pair = key.split('   ');
        var site_id = link_pair[0].slice(8);
        var note_id = link_pair[1].slice(8);
        var g1 = groups['g_site_' + site_id];
        var g2 = groups['g_note_' + note_id];
        var r  = rects['r_note_' + note_id];
        var link = make_note_link(svg, g1.select('circle'), r, line_weight,
                                  'groups_s_' + site_id + '_n_' + note_id);
        add_link_to_links(link, g1, g2);
    }
}

make_note_link = function(svg, c, r, weight, end_ids) {
    //TODO: utilize weight
    var link = svg.append("svg:line")
        .attr("x1", parseInt(c.attr("cx")))
        .attr("y1", parseInt(c.attr("cy")))
        .attr("x2", parseInt(r.attr("x")) + parseInt(r.attr("width")/2))
        .attr("y2", parseInt(r.attr("y")) + parseInt(r.attr("height")/2))
        .attr("class", "note_link")
        .attr("id", end_ids)
        .style("stroke", "#CCC");
    return link;
}

add_link_to_links = function(link, g1, g2) {
    id1 = g1.attr("id");
    id2 = g2.attr("id");
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
