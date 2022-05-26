import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    sys.stderr.write("Usage: {0} <file>.xml".format(sys.argv[0]))

XML_NODE_CONTENT = '_xml_node_content'
XML = 'xml:'
ATTRIBUTE = 'attribute: true'

f = open("converted.yaml", "w")


def yamlout(node, depth=0):
    if not depth:
        sys.stdout.write('---\n')
    # Nodes with both content AND nested nodes or attributes
    # have no valid yaml mapping. Add  'content' node for that case
    nodeattrs = node.attrib
    children = list(node)
    content = node.text.strip()if node.text else ' '
    if content:
        if not (nodeattrs or children):
            # Write as just a name value, nothing else nested

            # sys.stdout.write(
            #     '{indent}{tag}: {text}\n'.format(
            #         indent=depth * '  ', tag=node.tag, text=content or ''))
            f.write(
                '{indent}{tag}: \n  {indent}type: string\n  {indent}example: "{text}"\n'.format(
                    indent=depth * '  ', tag=node.tag, text=content.strip() or ''))
            return
        else:
            nodeattrs[XML_NODE_CONTENT] = node.text

    # sys.stdout.write('{indent}{tag}:\n'.format(
    #     indent=depth * '  ', tag=node.tag))
    f.write('{indent}{tag}:\n{indent} type: object\n {indent}properties:\n'.format(
        indent=depth * '  ', tag=node.tag))
    # f.write('{indent}{tag}:\n {indent}type: object\n {indent}properties:\n'.format(
    #     indent=depth * '  ', tag=node.tag))

    # Indicate difference node attributes and nested nodes
    depth += 1
    for n, v in nodeattrs.items():
        # sys.stdout.write(
        #     '{indent}{n}: {v} {c}\n'.format(
        #         indent=depth * '  ', n=n, v=v,
        #         c=XML if n != XML_NODE_CONTENT else ''))
        f.write(
            '{indent}{n}: \n {indent}type: string\n {indent}example: "{v}"\n {indent}{c}\n  {indent}{attb}\n'.format(
                indent=depth * '  ', n=n, v=v,
                c=XML if n != XML_NODE_CONTENT else '', attb=ATTRIBUTE if n != XML_NODE_CONTENT else ' '))
    # Write nested nodes
    for child in children:
        yamlout(child, depth)


with open('test_sample.xml') as xmlf:
    tree = ET.parse(xmlf)
    yamlout(tree.getroot())

f.close()
