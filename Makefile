.PHONY: sbom

sbom: sbom.cdx.json

sbom.cdx.json: uv.lock pyproject.toml
	uv export --no-hashes --no-editable --no-emit-project --frozen > /tmp/fiken-reqs.txt
	uvx --from cyclonedx-bom cyclonedx-py requirements /tmp/fiken-reqs.txt -o $@ --of json
