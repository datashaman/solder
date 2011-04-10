jQuery.fn.solder = function(source, map) {
    var othermap = map;
    return jQuery(this).each(function() {
        var that = this;
        jQuery.getJSON(source, {no_cache: Math.random}, function(data) {
            jQuery.each(data.rows, function(index, row) {
                map: function(parent, element, key, value) {
                    console.log(element);
                    switch(key) {
                        case 'username':
                            value = jQuery(scripts.link_to(value))[0];
                        break;

                        case 'email':
                            value = jQuery(scripts.email_to(value))[0]
                        break;
                    }

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
