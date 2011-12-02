from django import template

def parse_kw_args(tagname, bits, args_spec=None, restrict=False):
    """ keywords arguments parser for template tags

    returns a list of (argname, value) tuples
    (NB: keeps ordering and is easily turned into a dict).

    Params:
    * tagname : the name of calling tag (for error messages)
    * bits : sequence of tokens to parse as kw args
    * args_spec : (optional) dict of argname=>validator for kwargs, cf below
    * restrict : if True, only argnames in args_specs will be accepted

    If restrict=False and args_spec is None (default), this will just try
    to parse a sequence of key=val strings into a 

    About args_spec validators :
    * A validator can be either a callable, a regular expression or None.

    * If it's a callable, the callable must take the value as argument and
    return a (possibly different) value, which will become the final value
    for the argument. Any exception raised by the validator will be
    considered a rejection.

    * If it's a regexp, the value will be matched against it. A failure
    will be considered as a rejection.

    * Using None as validator only makes sense with the restrict flag set
    to True. This is useful when the only validation is on the argument
    name being expected.
    """

    args = []

    if restrict:
        if args_spec is None:
            raise ValueError("you must pass an args_spec dict if you want to restrict allowed args")
        allowed = list(args_spec.keys())
        do_validate = True
    else:
        do_validate = args_spec is not None

    for bit in bits:
        try:
            name, val = bit.split('=')
        except ValueError:
            raise template.TemplateSyntaxError(
                "keyword arguments to '%s' tag must have 'key=value' form (got : '%s')" \
                % (tagname, bit)
                )

        name = str(name)
        if do_validate:
            if restrict:
                if name in allowed:
                    # we only want each name once
                    del allowed[allowed.index(name)]
                else:
                    raise template.TemplateSyntaxError(
                        "keyword arguments to '%s' tag must be one of % (got : '%s')" \
                        % (tagname, ",".join(allowed), name)
                        )

                validate = args_spec[name]
            else:
                validate = args_spec.get(name, None)

            if validate is not None:
                if callable(validate):
                    try:
                        val = validate(val)
                    except Exception, e:
                        raise template.TemplateSyntaxError(
                            "invalid optional argument '%s' for '%s' tag: '%s' (%s)" \
                            % (tagname, name, val, e)
                            )
                else:
                    # assume re
                    if re.match(validate, val) is None:
                        raise template.TemplateSyntaxError(
                            "invalid optional argument '%s' for '%s' tag: '%s' (doesn't match '%s')" \
                            % (tagname, name, val, validate)
                        )

        # should be ok if we managed to get here        
        args.append((name, val))

    return args
