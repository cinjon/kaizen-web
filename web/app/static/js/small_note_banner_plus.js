$(function() {
    $('a.removeNote').unbind().click(function() {
        $.getJSON($(this).attr("url"), {
            noteId: $(this).closest('.controls-wrapper').children('.noteId').val(),
        }, function(data) {
            if (data.success) {
                var noteId = data.noteId;
                var siteNumNotes = data.siteNumNotes;
                var mapHasSites = data.mapHasSites;
                console.log(siteNumNotes);
                console.log(mapHasSites);

                if (!mapHasSites) {
                    // Redirect to /me
                }
                if (siteNumNotes == 0) {
                    // TODO(hide/remove site, activate a different one)
                } else {
                    // hide/remove note, reduce # of notes in site
                }

                $('#nid' + noteId).closest('.noteBanner').hide();
                $('#nid' + noteId).closest('.active').children('.smallbox').children('.row-fluid').children('.numNotes').html(siteNumNotes + " Notes");
            }
        });
        return false;
    });
});

$(function() {
    $('input.reindexNote').keyup(function(event){
        if(event.keyCode == 13){
            $.getJSON("{{ url_for('reindex_note') }}", {
                noteId: $(this).closest('.controls-wrapper').children('.noteId').val(),
                targetIndex: $(this).val(),
                mapId: $(this).closest('.controls-wrapper').children('.mapId').val()
            }, function(data) {
                window.console.log(data.result);
            });
        }
        return false;
    });
});
