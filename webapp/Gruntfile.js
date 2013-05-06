module.exports = function(grunt) {

    Array.prototype.contains = function (obj) {
        var i = this.length;
        while (i--) {
            if (this[i] === obj) {
                return true;
            }
        }
        return false;
    };

    function getFiles(srcdir, destdir, wildcard, ext, except) {
        var path = require('path');
        var files = {};
        grunt.file.expand({cwd: srcdir}, wildcard).forEach(function(relpath) {
        // console.log(relpath);
        if (except && !except.contains(relpath)) {
            files[path.join(destdir, relpath.split('.')[0] + '.' + ext)] = path.join(srcdir, relpath);
        }
        });
        // console.log(files);
        return files;
    }

    grunt.initConfig({
        pkg: '<json:package.json>',
        jade: {
            debug: {
                options: {
                    data: {
                        debug: true
                    }
                },
                files: getFiles('jade/', './', '**/*.jade', 'html', ['layout.jade', 'header.jade', 'footer.jade', 'alloc.jade', 'about.jade', 'contact.jade'])
            }
        },
        less: {
            production: {
                options: {
                    yuicompress: false
                },
                files: getFiles('less/', 'css/', '**/*.less', 'css', [])
            }
        },
        watch: {
            jade: {
                files: 'jade/*.jade',
                tasks: ['jade']
            },
            less: {
                files: 'less/*.less',
                tasks: ['less']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-jade');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['jade', 'less']);
};