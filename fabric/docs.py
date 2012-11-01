from fabric.tasks import WrappedCallableTask


def unwrap_tasks(module, hide_nontasks=False):
    """
    Replace task objects on ``module`` with their wrapped functions instead.

    Specifically, look for instances of `~fabric.tasks.WrappedCallableTask` and
    replace them with their ``.wrapped`` attribute (the original decorated
    function.)

    This is intended for use with the Sphinx autodoc tool, to be run near the
    bottom of a project's ``conf.py``. It ensures that the autodoc extension
    will have full access to the "real" function, in terms of function
    signature and so forth. Without use of ``unwrap_tasks``, autodoc is unable
    to access the function signature (though it is able to see e.g.
    ``__doc__``.)

    For example, at the bottom of your ``conf.py``::

        from fabric.docs import unwrap_tasks
        import my_package.my_fabfile
        unwrap_tasks(my_package.my_fabfile)

    You can go above and beyond, and explicitly **hide** all non-task
    functions, by saying ``hide_nontasks=True``. This renames all objects
    failing the "is it a task?" check so they appear to be private, which will
    then cause autodoc to skip over them.

    ``hide_nontasks`` is thus useful when you have a fabfile mixing in
    subroutines with real tasks and want to document *just* the real tasks.
    
    If you run this within an actual Fabric-code-using session (instead of
    within a Sphinx ``conf.py``), please seek immediate medical attention.

    .. versionadded: 1.5

    .. seealso:: `~fabric.tasks.WrappedCallableTask`, `~fabric.decorators.task`
    """
    for name, obj in vars(module).iteritems():
        if isinstance(obj, WrappedCallableTask):
            setattr(module, name, obj.wrapped)
        else:
            if hide_nontasks and getattr(obj, '__doc__', False):
                setattr(module, '_%s' % name, obj)
                delattr(module, name)
