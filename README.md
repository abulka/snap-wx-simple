# wxpython-actions-multi

Version: 1.94

Non beta - real

Latest versions can downloaded from https://github.com/abulka/wxpython-actions-multi/releases/latest

An experiment re checking out not only this project, but another project, then building an exe from combining the two.

On github, If we check out this project into `mainproj` then the other project into 

- subdir/mainproj/
- relationship_manager/

The reason for `subdir` is to locate this main project relative to `relationship_manager` the way it is on my development machine.

Then from 

    mainproj/src/simple.py

we should be able to find the package

    relationship_manager/relmgr

as long as cwd when running is 

    mainproj/src/
    
and as long as the PYTHONPATH is set to

    PYTHONPATH="../../../relationship-manager/"


Yikes, a bit convoluted. Would be easier to just import `relationship_manager` as a package using pip.

# Pyinstaller

Can build this OK, as I do it locally.  Spec file needs to be

```python
a = Analysis(['src/rubber_band_async.py'],
             pathex=[
                 '../../relationship-manager/',
             ], 

```

for Pyinstaller to find everything.

# Tags

In the workflow file:

- To trigger the workflow on each push, branches: [ main ]
- To trigger the workflow on push of tags beginning with v, tags: ['v*']

e.g.

```yml
name: multi project wxpython app built on mac
on:
  push:
    # branches: [ main ]
    tags: ['v*']
```

## To trigger a github actions workflow run

when you have set up workflow to run on tags eing pushed,

    git tag v1.0
    git push origin v1.0

or better, use an annotated tag (see explanation below)

    git tag -a v1.0
    git push --follow-tags

## To trigger via vscode commands
In vscode, creating a tag seems only to create a *lightweight* tag, unless you add a description.

- in vscode running the command `Git: Create Tag` - note entering a `message` when creating a tag via the UI will create an annotated tag
- in vsode running the command `Git: Push (follow tags)` 

## An aside on tags...

though interesting that `electron-actions1` has

    npm version patch
    git push --follow-tags

without an explicit tag push.  Why does `--follow-tags` work there but not here?

> The new " --follow-tags " option tells " git push " to push relevant annotated tags when pushing branches out. That won't push all the local tags though, only the one referenced by commits which are pushed with the git push .

Huh?

## Briliant explanation

https://vivaxyblog.github.io/2019/08/02/git-tag-and-push-git-tag.html

says

> Git supports two types of tags: lightweight and annotated.

> A lightweight tag is very much like a branch that doesn’t change — it’s just a pointer to a specific commit.

> Annotated tags, however, are stored as full objects in the Git database. They’re checksummed; contain the tagger name, email, and date; have a tagging message; and can be signed and verified with GNU Privacy Guard (GPG). It’s generally recommended that you create annotated tags so you can have all this information; but if you want a temporary tag or for some reason don’t want to keep the other information, lightweight tags are available too.

    git tag <tagname>                 => lightweight tag
    git tag -a <tagname>              => annotated tag, will prompt for mesage
    git tag -a -m <msg> <tagname>     => annotated tag
    git tag -m <msg> <tagname>        => annotated tag

There are two ways of pushing tags:

- git push --follow-tags
- git push --tags

> `git push --follow-tags`
> 
> It pushes both commits and only tags that are both:
> 
> *   annotated
> *   reachable (an ancestor) from the pushed commits
> 
> This is sane because:
> 
> *   you should only push annotated tags to the remote, and keep lightweight tags for local development to avoid tag clashes. See also: [What is the difference between an annotated and unannotated tag?](https://stackoverflow.com/questions/11514075/what-is-the-difference-between-an-annotated-and-unannotated-tag)
> *   it won’t push annotated tags on unrelated branches
> 
> It is for those reasons that –tags should be avoided.


How do we push tags? `git push --follow-tags`!

### In Conclusion

When you can’t push tags, you probably:

- are using a lightweight tag, and `git push --follow-tags`.

While you can push tags, you probably:

- are using a lightweight tag, and `git push --tags`. (Not recommended!)
- are using an annotated tag, and `git push --follow-tags`.

## Andy Summary of tags:
Two types of tags, lightweight (normal) and annotated. 

Use lightweight for local, and don't pollute the remote with these.

For remote use pass `-a` when creating a tag, 

    git tag -a <tagname>              => annotated tag, will prompt for mesage
    git tag -a -m <msg> <tagname>     => annotated tag

and it will be pushed when you

    git push --follow-tags


# action-gh-release@v1 - wildcards

When referring to artifacts that are really directories (e.g. mac .app) you might get an error
🤔 rubber-band-macos-v1.85,rubber-band-windows-v1.85 not include valid file. 
This is because these are actually artifact directories! 
You need to add `/*` to grab the directory contents. E.g. this works ok:
```yml
- name: Release
    uses: softprops/action-gh-release@v1
    env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    with:
    files: |
        rubber-band-macos-${{ env.TAG }}/*
        rubber-band-windows-${{ env.TAG }}/*
```
