import yaml
import argparse


def recursve_include(template):
    includes = template.get("Resources", {}).get("Include", [])
    
    if not includes:
        return template

    for include_key in includes:
        with open(include_key) as f:
            print(f"Loading {include_key}")
            include_template = yaml.load(f, Loader=yaml.BaseLoader)
            template["Resources"].update(include_template["Resources"].items())

    del template["Resources"]["Include"]
    return template


def main(
    template_file: str = "better-template.yaml", output_file: str = "template.yaml"
):
    with open(template_file) as f:
        template = yaml.load(f, Loader=yaml.BaseLoader)

    # Look for Include in the better-template.yaml in any place and then append the data by loading the templte file
    new_template = recursve_include(template)

    with open(output_file, "w") as f:
        yaml.dump(new_template, f, sort_keys=False)

    print(f"Output written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-file", default="better-template.yaml")
    parser.add_argument("--output-file", default="template.yaml")
    args = parser.parse_args()

    main(args.template_file, args.output_file)
