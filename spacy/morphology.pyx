# cython: infer_types
import numpy
import warnings
from cython.operator cimport dereference as deref
from libcpp.memory cimport unique_ptr
from libcpp.utility cimport move

from .errors import Warnings
from . import symbols


cdef class Morphology:
    """Store the possible morphological analyses for a language, and index them
    by hash.

    To save space on each token, tokens only know the hash of their
    morphological analysis, so queries of morphological attributes are delegated
    to this class.
    """
    FEATURE_SEP = "|"
    FIELD_SEP = "="
    VALUE_SEP = ","
    # not an empty string so we can distinguish unset morph from empty morph
    EMPTY_MORPH = symbols.NAMES[symbols._]

    def __init__(self, StringStore strings):
        self.strings = strings

    def __reduce__(self):
        tags = set([self.get(self.strings[s]) for s in self.strings])
        tags -= set([""])
        return (unpickle_morphology, (self.strings, sorted(tags)), None, None)

    cdef const MorphAnalysisC* _lookup_tag(self, hash_t tag_hash):
        match = self.tags.find(tag_hash)
        if match != self.tags.const_end():
            return deref(match).second.get()
        else:
            return NULL

    def _normalize_attr(self, attr_key, attr_value):
        if isinstance(attr_key, (int, str)) and isinstance(attr_value, (int, str)):
            attr_key = self.strings.as_string(attr_key)
            attr_value = self.strings.as_string(attr_value)

            # Preserve multiple values as a list
            if self.VALUE_SEP in attr_value:
                values = attr_value.split(self.VALUE_SEP)
                values.sort()
                    attr_value = values
        else:
            warnings.warn(Warnings.W100.format(feature={attr_key: attr_value}))
            return None

        return attr_key, attr_value

    def _str_to_normalized_feat_dict(self, feats):
        if not feats or feats == self.EMPTY_MORPH:
            return {}

        out = []
        for feat in feats.split(self.FEATURE_SEP):
            field, values = feat.split(self.FIELD_SEP)
            normalized_attr = self._normalize_attr(field, values)
            if normalized_attr is None:
                continue
            out.append((normalized_attr[0], normalized_attr[1]))
        out.sort(key=lambda x: x[0])
        return dict(out)

    def _dict_to_normalized_feat_dict(self, feats):
        out = []
        for field, values in feats.items():
            normalized_attr = self._normalize_attr(field, values)
            if normalized_attr is None:
                continue
            out.append((normalized_attr[0], normalized_attr[1]))
        out.sort(key=lambda x: x[0])
        return dict(out)


    def _normalized_feat_dict_to_str(self, feats):
        norm_feats_string = self.FEATURE_SEP.join([
                self.FIELD_SEP.join([field, self.VALUE_SEP.join(values) if isinstance(values, list) else values])
            for field, values in feats.items()
        ])
        return norm_feats_string or self.EMPTY_MORPH


    cdef hash_t _add(self, features):
        """Insert a morphological analysis in the morphology table, if not
        already present. The morphological analysis may be provided in the UD
        FEATS format as a string or in the tag map dict format.
        Returns the hash of the new analysis.
        """
        cdef hash_t hash = 0
        cdef const MorphAnalysisC* tag = NULL
        if isinstance(features, str):
            if features == "":
                features = self.EMPTY_MORPH

            hash = self.strings[features]
            tag = self._lookup_tag(hash)
            if tag is not NULL:
                return tag.key

            features = self._str_to_normalized_feat_dict(features)
        elif isinstance(features, dict):
            features = self._dict_to_normalized_feat_dict(features)
        else:
            warnings.warn(Warnings.W100.format(feature=features))
            features = {}

        # the hash key for the tag is either the hash of the normalized UFEATS
        # string or the hash of an empty placeholder
        norm_feats_string = self._normalized_feat_dict_to_str(features)
        hash = self.strings.add(norm_feats_string)
        tag = self._lookup_tag(hash)
        if tag is not NULL:
            return tag.key

        self._intern_morph_tag(hash, features)
        return hash

    cdef void _intern_morph_tag(self, hash_t tag_key, feats):
        # intified ("Field", "Field=Value") pairs where fields with multiple values have
        # been split into individual tuples, e.g.:
        # [("Field1", "Field1=Value1"), ("Field1", "Field1=Value2"),
        # ("Field2", "Field2=Value3")]
        field_feature_pairs = []

        # Feat dict is normalized at this point.
        for field, values in feats.items():
            field_key = self.strings.add(field)
            if isinstance(values, list):
            for value in values:
                value_key = self.strings.add(field + self.FIELD_SEP + value)
                field_feature_pairs.append((field_key, value_key))
            else:
                value_key = self.strings.add(field + self.FIELD_SEP + values)
                field_feature_pairs.append((field_key, value_key))

        num_features = len(field_feature_pairs)
        cdef unique_ptr[MorphAnalysisC] tag = unique_ptr[MorphAnalysisC](new MorphAnalysisC())
        deref(tag).key = tag_key
        deref(tag).features.resize(num_features)

        for i in range(num_features):
            deref(tag).features[i].field = field_feature_pairs[i][0]
            deref(tag).features[i].value = field_feature_pairs[i][1]

        self.tags[tag_key] = move(tag)

    cdef str get_morph_str(self, hash_t morph_key):
        cdef const MorphAnalysisC* tag = self._lookup_tag(morph_key)
        if tag is NULL:
            return ""
        else:
            return self.strings[tag.key]

    cdef const MorphAnalysisC* get_morph_c(self, hash_t morph_key):
        return self._lookup_tag(morph_key)

    cdef str _normalize_features(self, features):
        """Create a normalized FEATS string from a features string or dict.

        features (Union[dict, str]): Features as dict or UFEATS string.
        RETURNS (str): Features as normalized UFEATS string.
        """
        if isinstance(features, str):
            features = self._str_to_normalized_feat_dict(features)
        elif isinstance(features, dict):
            features = self._dict_to_normalized_feat_dict(features)
        else:
            warnings.warn(Warnings.W100.format(feature=features))
            features = {}

        return self._normalized_feat_dict_to_str(features)

    def add(self, features):
        return self._add(features)

    def get(self, morph_key):
        return self.get_morph_str(morph_key)

    def normalize_features(self, features):
        return self._normalize_features(features)   

    @staticmethod
    def feats_to_dict(feats):
        if not feats or feats == Morphology.EMPTY_MORPH:
            return {}
        return {field: Morphology.VALUE_SEP.join(sorted(values.split(Morphology.VALUE_SEP))) for field, values in
                [feat.split(Morphology.FIELD_SEP) for feat in feats.split(Morphology.FEATURE_SEP)]}

    @staticmethod
    def dict_to_feats(feats_dict):
        if len(feats_dict) == 0:
            return ""
        return Morphology.FEATURE_SEP.join(sorted([Morphology.FIELD_SEP.join([field, Morphology.VALUE_SEP.join(sorted(values.split(Morphology.VALUE_SEP)))]) for field, values in feats_dict.items()]))


cdef int check_feature(const MorphAnalysisC* morph, attr_t feature) nogil:
    cdef int i
    for i in range(morph.features.size()):
        if morph.features[i].value == feature:
            return True
    return False


cdef list list_features(const MorphAnalysisC* morph):
    cdef int i
    features = []
    for i in range(morph.features.size()):
        features.append(morph.features[i].value)
    return features


cdef np.ndarray get_by_field(const MorphAnalysisC* morph, attr_t field):
    cdef np.ndarray results = numpy.zeros((morph.features.size(),), dtype="uint64")
    n = get_n_by_field(<uint64_t*>results.data, morph, field)
    return results[:n]


cdef int get_n_by_field(attr_t* results, const MorphAnalysisC* morph, attr_t field) nogil:
    cdef int n_results = 0
    cdef int i
    for i in range(morph.features.size()):
        if morph.features[i].field == field:
            results[n_results] = morph.features[i].value
            n_results += 1
    return n_results

def unpickle_morphology(strings, tags):
    cdef Morphology morphology = Morphology(strings)
    for tag in tags:
        morphology.add(tag)
    return morphology
