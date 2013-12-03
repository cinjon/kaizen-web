$(function() {
    $('a.removeNote').bind('click', function() {
        $.getJSON("{{ url_for('remove_index') }}", {
            loopId: $(this).closest('.controls-wrapper').children('.loopId').val(),
            mapId: $(this).closest('.controls-wrapper').children('.mapId').val()
        }, function(data) {
            window.console.log(data.result);
        });
        return false;
    });
});

$(function() {
    $('input.reindexNote').keyup(function(event){
        if(event.keyCode == 13){
            $.getJSON("{{ url_for('reindex_note') }}", {
                loopId: $(this).closest('.controls-wrapper').children('.loopId').val(),
                targetIndex: $(this).val(),
                mapId: $(this).closest('.controls-wrapper').children('.mapId').val()
            }, function(data) {
                window.console.log(data.result);
            });
        }
        return false;
    });
});
