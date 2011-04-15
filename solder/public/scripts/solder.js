jQuery.fn.solder = function(source) {
    link_to = function(v) {
        return jQuery('<a href="' + v.url + '">' + v.username + '</a>').get(0);
    }

    email_to = function(v) {
        return jQuery('<a href="mailto:' + v.email + '">' + v.email + '</a>').get(0);
    }

    my_map = function(row) {
        row.link_to = link_to(row);
        row.email_to = email_to(row);
        return row;
    }

    index = this.index();
    parent = this.parent();
    original = this.remove();

    set_value = function(el, value) {
      if(el.tagName == 'INPUT') {
        jQuery(el).val(value);
      } else {
        jQuery(el).html(value);
      }
    };

    return jQuery(this).each(function() {
        jQuery.getJSON(source, {no_cache: Math.random}, function(data) {
            if('record' in data) {
               record = my_map(data.record);
               jQuery(data.metadata).each(function(_, column) {
                    if(column.display != false) {
                        element = original.clone();
                        parent.append(element);

                        element.find('.label').each(function(_, el) {
                            set_value(el, column.label);
                        });
                        element.find('.value').each(function(_, el) {
                            console.log(data.record, column.name);
                            set_value(el, record[column.name]);
                        });
                    }
                });
            } else {
                jQuery(data.rows).each(function(index, row) {
                    element = original.clone();
                    parent.append(element);

                    row = my_map(row);

                    for(name in row) {
                        value = row[name];
                        element.find('.'+name).each(function(index, el) { set_value(el, value); });
                    }
                });
            }
        });
    });
};
