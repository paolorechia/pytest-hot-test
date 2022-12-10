
class HotTestPluginError(Exception):
    pass

class DependencyTrackingError(Exception):
    pass

class SourcePathNotSet(DependencyTrackingError):
    pass

class InvalidSourcePath(DependencyTrackingError):
    pass