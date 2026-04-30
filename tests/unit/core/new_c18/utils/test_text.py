"""
Unit tests for src/core/new_c18/utils/text.py module.
TODO: write tests
"""
from src.core.new_c18.utils.text import extract_wikidata_qid


class TestExtractWikidataQid:
    """Tests for extract_wikidata_qid function"""

    def test_extracts_qid_from_wikidata_template(self):
        """Test extracting QID from قيمة ويكي بيانات template"""
        text = "{{قيمة ويكي بيانات/قالب تحقق|Q12345}}"
        result = extract_wikidata_qid(text)
        assert result == "Q12345"

    def test_extracts_qid_with_id_parameter(self):
        """Test extracting QID with id= parameter"""
        text = "{{قيمة ويكي بيانات/قالب تحقق|id=Q67890}}"
        result = extract_wikidata_qid(text)
        assert result == "Q67890"

    def test_extracts_qid_from_cycling_race_template(self):
        """Test extracting QID from cycling race template"""
        text = "{{سباق الدراجات/صندوق معلومات|Q11111}}"
        result = extract_wikidata_qid(text)
        assert result == "Q11111"

    def test_extracts_qid_from_english_cycling_template(self):
        """Test extracting QID from English cycling template"""
        text = "{{Cycling race/infobox|Q22222}}"
        result = extract_wikidata_qid(text)
        assert result == "Q22222"

    def test_returns_none_when_no_qid(self):
        """Test that None is returned when no QID found"""
        text = "مقالة عادلة بدون قالب ويكي بيانات"
        result = extract_wikidata_qid(text)
        assert result is None

    def test_returns_none_for_empty_text(self):
        """Test that None is returned for empty text"""
        result = extract_wikidata_qid("")
        assert result is None

    def test_handles_multiple_templates(self):
        """Test that first matching QID is extracted"""
        text = "{{قيمة ويكي بيانات/قالب تحقق|Q111}}{{قيمة ويكي بيانات/قالب تحقق|Q222}}"
        result = extract_wikidata_qid(text)
        assert result == "Q111"
