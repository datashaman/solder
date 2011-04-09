jQuery.fn.solder = function(source, map) {
    var othermap = map;
    return jQuery(this).each(function() {
        var that = this;
        jQuery.getJSON(source, {no_cache: Math.random}, function(data) {
            window.weld(that, data.rows, {
                map: function(parent, element, key, value) {
                    jQuery.each(data.metadata, function(index, column) {
                        switch(column.name) {
                            case key:
                                value = column.html ? jQuery(value)[0] : value;
                            break;

                            case 'username':
                                value = scripts.link_to(value);
                            break;

                            case 'email':
                                value = scripts.email_to(value);
                            break;
                        }
                    });

                    if(typeof othermap != 'function')
                        return value;

                    console.log('here with ' + this + ' and ' + that);

                    return othermap(parent, element, key, value);
                }
            });
        });
    });
};

scripts = {
    link_to: function(v) {
        return $('<a href="' + v.url + '">' + v.username + '</a>').html();
    },
    email_to: function(v) {
        return $('<a href="mailto:' + v.email + '">' + v.email + '</a>').html();
    }
}
