$(document).ready(function() {
    $('#filter-user').select2({
      ajax: {
        url: "/audit/users_autocompletion",
        dataType: 'json',
        delay: 250,
        data: function(params) {
          return {
            q: params.term, // search term
          };
        },
        processResults: function(data) {
          return {
            results: data.results,
          };
        },
        cache: true,
      },
      minimumInputLength: 1, // Require at least 1 character to search
      allowClear: true, // Enables clearable option
    });
});