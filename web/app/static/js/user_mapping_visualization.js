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
var links, update_links, notes, sites;
var mapdata;
var connect_tool_state, delete_obj_tool_state;

function showMappingVisualization(server_data, show) {
    if (server_data && show) {
        mapdata = server_data;
        start_map_sandlot();
        display_root();
    }
}

start_map_sandlot = function() {
    set_initial_conditions($("#map-sandlot"));
    svg = d3.select("#map-sandlot")
        .append("svg:svg")
        .style("width", width)
        .style("height", height);

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
    set_tool_states = function() {
        connect_tool_state = false;
        delete_obj_tool_state = false;
    }
    set_objects = function() {
        links = {};
        update_links = {'del':{}, 'add':{}};
        notes = {};
        sites = {};
    }

    set_dimensions(sandlot);
    set_objects();
    set_tool_states();
};

is_connect_node = function(node) {
    if (connect_tool_state && node.attr("class").indexOf("connect_from") !== -1) {
        return true;
    }
    return false;
}

is_connected = function(node_s, node_e) {
    //Change later to differentiate between direction
    id_s = node_s.attr("id");
    id_e = node_e.attr("id");
    if (id_s == id_e || (id_e in links && id_s in links[id_e]) || (id_s in links && id_e in links[id_s])) {
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

$(function() {
    $('#add_connect_tool').bind('click', add_connect_tool_click);
});

$(function() {
    $('#delete_obj_tool').bind('click', del_obj_tool_click);
});

$(function() {
    $('#save_state_tool').bind('click', save_state_tool_click);
});

add_connect_tool_click = function() {
    if (!connect_tool_state) {
        connect_tool_state = true;
        $("#add_connect_tool").text("Connect On");
        turn_off_delete_tool();
    } else {
        turn_off_connect_tool();
    }
}

deactivate_button = function (_id, txt) {
    var button = $("#" + _id);
    if (button.attr("class").indexOf("active") !== -1) {
        button.button('toggle');
    }
    if (txt) {
        button.text(txt);
    }
}

turn_off_connect_tool = function() {
    if (connect_tool_state) {
        connect_tool_state = false;
        deactivate_button("add_connect_tool", "Connect Off");
    }
    var connect_tool_node = $('[class*="connect_node"]');
    if (connect_tool_node.length > 0) {
        //TODO(css fix) --> This is not working as it should.
        var node_class = connect_tool_node.attr("class");
        connect_tool_node.attr("class", node_class.slice(0, -13));
        connect_tool_node.attr("fill", "wheat");
    }
}

del_obj_tool_click = function() {
    if (!delete_obj_tool_state) {
        delete_obj_tool_state = true;
        $("#delete_obj_tool").text("Delete On");
        turn_off_connect_tool();
    } else {
        turn_off_delete_tool();
    }
}

turn_off_delete_tool = function() {
    if (delete_obj_tool_state) {
        delete_obj_tool_state = false;
        deactivate_button("delete_obj_tool", "Delete Off");
    }
}

save_state_tool_click = function() {
    $.post($SCRIPT_ROOT + '/save_state', {
        'vid'   : JSON.stringify(mapdata.mapping.mid),
        'sites' : JSON.stringify(_save_nodes_json(sites, 'sites')),
        'notes' : JSON.stringify(_save_nodes_json(notes, 'notes')),
        'root'  : JSON.stringify(_root_json()),
        'links' : JSON.stringify(update_links)
    }, function(response) {
        deactivate_button("save_state_tool");
    });
    return false;
}

_position_from_dom = function(dom) {
    return {'x':parseInt(dom.attr("link_x")), 'y':parseInt(dom.attr("link_y"))};
}

_dom_has_moved = function(original_position, dom) {
    var new_position = _position_from_dom(dom);
    if (dom.attr("class").indexOf("noteNode") !== -1) {
        new_position.x = new_position.x + parseInt(dom.attr("width")/2);
        new_position.y = new_position.y + parseInt(dom.attr("height")/2);
    }
    if ((new_position.x != original_position[0] || new_position.y != original_position[1])) {
        return [new_position.x, new_position.y];
    }
    return false;
}

_save_nodes_json = function(nodes, ty) {
    var _id, node, ret;
    ret = {};
    for (_id in nodes) {
        node = nodes[_id];
        if (node.deleted) {
            ret[_id] = 'deleted';
        } else {
            var _moved = _dom_has_moved(mapdata[ty][_id].position, $('#' + _id));
            if (_moved) {
                ret[_id] = {'x':_moved[0], 'y':_moved[1]};
            }
        }
    }
    return ret;
}

_root_json = function() {
    var _id, _moved, ret
    _id = mapdata.root._id;
    _moved = _dom_has_moved(mapdata.root.position, $('#' + _id));
    ret = {};
    if (_moved) {
        ret[_id] = {'x':_moved[0], 'y':_moved[1]};
    }
    return ret;
}

display_root = function() {
    $("#rootTitle").html(mapdata.mapping.name);
    $("#rootCountSites").html("<p>Sites: " + Object.size(sites) + "</p>");
    $("#rootCountNotes").html("<p>Notes: " + Object.size(notes) + "</p>");
    $("#map-site").hide();
    $("#map-note").hide();
    $("#map-root").show();
}

display_note = function(_id) {
    data = notes[_id];
    $("#noteId").val(data.nid);
    $("#mapId").val(mapdata.mapping.mid);
    $("#noteTime").html('<em><small class="muted">' + data.creation_time + '</small></em>')
    $("#noteText").html(data.text);
    $("#noteUrl").attr("title", data.url).html('<a target="_blank" href="' + data.url + '">' + data.url.slice(0, 40) + '</a>')
    $("#noteName").html(data.nid); //change to data.name when allowing users to submit
    $("#map-site").hide();
    $("#map-root").hide();
    $("#map-note").show();
}

display_site = function(_id) {
    data = sites[_id];
    $("#siteId").val(data.sid);
    $("#siteTitle").html(data.title);
    $("#siteUrl").attr("title", data.url).html('<a target="_blank" href="' + data.url + '">' + data.url.slice(0, 40) + '</a>')
    $("#siteTime").html(data.creation_time);
    $("#map-note").hide();
    $("#map-root").hide();
    $("#map-site").show();
}

drag = function(move) {
    return d3.behavior.drag().on("drag", move);
}

move_links = function(node) {
    nodelinks = links[node.attr("id")];
    for (var link_id in nodelinks) {
        var link = $("#" + link_id);
        var end  = nodelinks[link_id];
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
    click_func = function() {return click(display_root, maproot._id);};
    circle = svg.append("svg:circle")
        .attr("class", "rootNode")
        .attr("id", maproot._id)
        .attr("cx", maproot.position[0]).attr("link_x", maproot.position[0])
        .attr("cy", maproot.position[1]).attr("link_y", maproot.position[1])
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
        console.log('mapsites with key ' + key + ', ' + mapsites[key] + ', ' + mapsites[key].site);
        sites[key] = mapsites[key].site;
        sites[key].x = mapsites[key].position[0]
        sites[key].y = mapsites[key].position[1]
    }
}

make_site = function(_id, name, position, radius) {
    var circle, text, click_func;
    click_func = function() {return click(display_site, _id);};
    circle = svg.append("svg:circle")
        .attr("class", "siteNode")
        .attr("id", _id)
        .attr("r", radius)
        .attr("cx", position[0])
        .attr("cy", position[1])
        .attr("link_x", position[0])
        .attr("link_y", position[1])
        .attr("fill", "wheat") //#0772A1
        .attr("opacity", .8)
        .on("click", click_func)
        .on("mouseover", function() {mouseover(d3.select(this), "gray");})
        .on("mouseout", function() {mouseout(d3.select(this), "wheat");})
        .call(drag(move_site));
    text = make_node_text("t" + _id, name, position[0]-radius, position[1], click_func);
}

make_notes = function(mapnotes) {
    for (var key in mapnotes) {
        make_note(key, key, mapnotes[key].position, mapnotes[key].radius);
        notes[key] = mapnotes[key].note;
        notes[key].x = mapnotes[key].position[0];
        notes[key].y = mapnotes[key].position[1];
    }
}

make_note = function(_id, name, position, radius) {
    var side = 30;
    var click_func = function() {return click(display_note, _id);};
    var rect = svg.append("svg:rect")
        .attr("class", "noteNode")
        .attr("id", _id)
        .attr("x", position[0] - side/2)
        .attr("y", position[1] - side/2)
        .attr("link_x", position[0])
        .attr("link_y", position[1])
        .attr("width", side)
        .attr("height", side)
        .attr("fill", "wheat") //rgb(6,120,155)
        .attr("rx", 7)
        .attr("ry", 7)
        .attr("stroke-width", 5)
        .attr("opacity", .6)
        .on("click", click_func)
        .on("mouseover", function() {mouseover(d3.select(this), "gray");})
        .on("mouseout", function() {mouseout(d3.select(this), "wheat");})
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

click = function(_default_click, _id) {
    if (connect_tool_state) {
        return connect_node(_id);
    } else if (delete_obj_tool_state) {
        return delete_obj(_id);
    } else if (_default_click) {
        return _default_click(_id);
    }
    return;
}

_get_connect_node_attr = function(node) {
    var _id, link_x, link_y;
    _id = node.attr("id");
    link_x = parseInt(node.attr("link_x"));
    link_y = parseInt(node.attr("link_y"));
    return {'x':link_x, 'y':link_y, 'id':_id};
}

connect_node = function(_id) {
    if (_id.indexOf('_') !== -1) {
        return; //it's a link
    }

    var node = $("#" + _id);
    var connect_tool_node = $('[class*="connect_node"]');
    if (connect_tool_node.length == 0) {
        var node_class = node.attr("class");
        node.attr("class", node_class + " connect_node");
        node.attr("fill", "#FF0000");
    } else if (!is_connected(node, connect_tool_node)) {
        start_node_attr = _get_connect_node_attr(connect_tool_node);
        end_node_attr   = _get_connect_node_attr(node);
        make_link(start_node_attr.x, start_node_attr.y,
                  end_node_attr.x, end_node_attr.y,
                  start_node_attr.id, end_node_attr.id);
        _update_links('del', 'add', start_node_attr.id + '_' + end_node_attr.id);
        turn_off_connect_tool();
    }
}

delete_obj = function(_id) {
    var obj = $("#" + _id);
    if (obj.attr("class") == "link") {
        _delete_link(obj, _id);
    } else if (obj.attr("class") == "noteNode" || obj.attr("class") == "siteNode") {
        _delete_node(obj, _id, obj.attr("class").slice(0,4));
    }
};

_update_links = function(remove_from_ty, add_to_ty, _id) {
    if (_id in update_links[remove_from_ty]) {
        delete update_links[remove_from_ty][_id];
    } else {
        update_links[add_to_ty][_id] = true;
    }
}

_delete_link = function(link, _id) {
    var end_ids = _id.split('_');
    delete links[end_ids[0]][_id];
    delete links[end_ids[1]][_id];
    _update_links('add', 'del', _id);
    link.remove();
}

_delete_node = function(node, _id, ty) {
    if (ty == "site") {
        sites[_id].deleted = true;
    } else if (ty == "note") {
        notes[_id].deleted = true;
    } else {
        return;
    }

    for (var link_id in links[_id]) {
        delete_obj(link_id);
    }
    $("#t" + _id).remove();
    node.remove();
}

make_links = function(maplinks) {
    for (var index in maplinks) {
        var maplink = maplinks[index];
        var _id1 = maplink[0];
        var _id2 = maplink[3];
        make_link(maplink[1], maplink[2],
                  maplink[4], maplink[5],
                  _id1, _id2, maplink[6]);
    }
}

make_link = function(e1x, e1y, e2x, e2y, e1id, e2id, weight) {
    //TODO utilize weight
    //would be good to do something visually with the ends when you click the link
    var _id = e1id + '_' + e2id;
    var click_func = function() {return click(null, _id);};
    var link = svg.append("svg:line")
        .attr("x1", e1x)
        .attr("y1", e1y)
        .attr("x2", e2x)
        .attr("y2", e2y)
        .attr("class", "link")
        .attr("id", _id)
        .style("stroke", "#3E97D1")
        .style("stroke-width", 5)
        .style("stroke-opacity", .3)
        .on("mouseover", function() {mouseover(d3.select(this), "#A60000");})
        .on("mouseout", function() {mouseout(d3.select(this), "#3E97D1");})
        .on("click", click_func);
    add_link_to_links(link, e1id, e2id);
    return link;
}

add_link_to_links = function(link, id1, id2) {
    if (!(id1 in links)) {
        links[id1] = {}
    }
    if (!(id2 in links)) {
        links[id2] = {};
    }
    links[id1][link.attr("id")] = '1';
    links[id2][link.attr("id")] = '2';
}

$(function() {
    $('input.nameNote').keyup(function(event){
        if(event.keyCode == 13){
            $.getJSON("{{ url_for('name_note') }}", {
                noteId: $("#noteId").val(),
                newName: $(this).val()
            }, function(data) {
                window.console.log(data.result);
            });
        }
        return false;
    });
});

$(function() {
    $('input.nameSite').keyup(function(event){
        if(event.keyCode == 13){
            $.getJSON("{{ url_for('name_site') }}", {
                noteId: $("#siteId").val(),
                newName: $(this).val()
            }, function(data) {
                //do something with return
                window.console.log(data.result);
            });
        }
        return false;
    });
});

$(function() {
    $('a.deleteNote').bind('click', function() {
        $.getJSON("{{ url_for('delete_note') }}", {
            noteId: $(this).closest('.controls-wrapper').children('.noteId').val()
        }, function(data) {
            window.console.log(data.result);
        });
        return false;
    });
});

$(function() {
    $('a.deleteSite').bind('click', function() {
        $.getJSON("{{ url_for('delete_site') }}", {
            siteId: $(this).closest('.controls-wrapper').children('.siteId').val()
        }, function(data) {
            //remove Stuff from svg here
        });
        return false;
    });
});

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
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
