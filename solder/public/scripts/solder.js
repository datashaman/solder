jQuery.fn.solder = function(source) {
    link_to = function(href, text) {
        return jQuery('<a href="' + href + '">' + text + '</a>').get(0);
    }

    email_to = function(email, text) {
        if(typeof text == "undefined")
            text = email;
        return jQuery('<a href="mailto:' + email + '">' + text + '</a>').get(0);
    }

    generate_data = function(scripts, record) {
        for(name in scripts) {
            script = scripts[name];
            record[name] = eval(script);
        }
        return record;
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
            jQuery(data.records).each(function(index, record) {
                element = original.clone();
                parent.append(element);

                record = generate_data(data.scripts, record);

                for(name in record) {
                    value = record[name];
                    element.find('.'+name).each(function(index, el) { set_value(el, value); });
                }
            });
        });
    });
};
