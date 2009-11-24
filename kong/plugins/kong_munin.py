from kong.models import TestResult, Test
import munin

def slugify(string):
    return string.replace('-','_')

class KongDuration(munin.Plugin):
    tests = Test.objects.all()

    def fetch(self):
        limit = len(self.tests) - 1
        results = TestResult.objects.filter(site__pk=2)[:limit]
        for result in results:
            yield ('%s.value' % slugify(result.test.slug), result.duration)
    
    def config(self):
        yield ('graph_title', 'LJWorld')
        yield ('graph_args', '-l 0 --base 1000')
        yield ('graph_vlabel', 'Duration')
        yield ('graph_scale', 'no')
        yield ('graph_category', 'kong')
        yield ('graph_info', 'Shows the duration of Kong tests.')
        for test in  self.tests:
            yield ("%s.label" % slugify(test.slug), test.name)
            yield ("%s.info" % slugify(test.slug), test.name)
            yield ("%s.draw" % slugify(test.slug), "LINE1")
 
if __name__ == '__main__':
    munin.run(KongDuration)
