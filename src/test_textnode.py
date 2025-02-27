import unittest

from textnode import (TextNode, 
TextType, 
split_nodes_delimiter, 
extract_markdown_images, 
extract_markdown_links, 
split_nodes_image, 
split_nodes_link,
text_to_textnodes)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        node2 = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        node2 = TextNode("Text node with URL", TextType.ITALIC, "https://www.gitlab.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_2(self):
        node = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        node2 = TextNode("Text node with URL", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("Did you ever hear the tragedy of Darth Plagueis the Wise?", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_just_text_single_node(self):
        nodes = [TextNode("this is just text without delimiters", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.TEXT)
        self.assertEqual(new_nodes[0], TextNode("this is just text without delimiters", TextType.TEXT))

    def test_other_text_type(self):
        nodes = [TextNode("this is just text without delimiters", TextType.CODE)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("this is just text without delimiters", TextType.CODE))

    def test_no_delimitires_in_node(self):
        nodes = [TextNode("this is just text without delimiters", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("this is just text without delimiters", TextType.TEXT))

    def test_code_delimiter_single_node(self):
        nodes = [TextNode("this is text with a 'code block'", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))

    def test_italic_delimiter_single_node(self):
        nodes = [TextNode("there are *italic words* in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes[1], TextNode("italic words", TextType.ITALIC))

    def test_bold_delimiter_single_node(self):
        nodes = [TextNode("there are **bold words** in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[1], TextNode("bold words", TextType.BOLD))

    def test_code_multiple_delimiters_single_node(self):
        nodes = [TextNode("this text has 'one code block' and then 'another code block'", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
        expected_nodes = [
            TextNode("this text has ", TextType.TEXT), 
            TextNode("one code block", TextType.CODE),
            TextNode(" and then ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_italic_multiple_delimites_single_node(self):
        nodes = [TextNode("there are *italic words* and *more italic words* in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("there are ", TextType.TEXT), 
            TextNode("italic words", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("more italic words", TextType.ITALIC),
            TextNode(" in this text", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_bold_multiple_delimiters_single_node(self):
        nodes = [TextNode("there are **bold words** and **more bold words** in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("there are ", TextType.TEXT), 
            TextNode("bold words", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold words", TextType.BOLD),
            TextNode(" in this text", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_code_multiple_nodes(self):
        nodes = [
            TextNode("First text node with a 'code block'", TextType.TEXT), 
            TextNode("Second text node with 'another code block'", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
        expected_nodes = [
            TextNode("First text node with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE),
            TextNode("Second text node with ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            ]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_italics_multiple_nodes(self):
        nodes = [
            TextNode("This text node has *italic* words", TextType.TEXT), 
            TextNode("Second text node also has words in *italic*", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This text node has ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT),
            TextNode("Second text node also has words in ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_bold_multiple_nodes(self):
        nodes = [
            TextNode("This text node has **bold** words", TextType.TEXT), 
            TextNode("Second text node also has words in **bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This text node has ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
            TextNode("Second text node also has words in ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_one_image(self):
        text = "This is a text with ![an F-16 fighter jet](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg)"
        expected_output = [("an F-16 fighter jet", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_multiple_images(self):
        text = "This is a text with ![an F-16 fighter jet](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg) and ![Godzilla](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg)"
        expected_output = [
            ("an F-16 fighter jet", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg"), 
            ("Godzilla", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_one_link(self):
        text = "This is a text with a link [to Google](https://www.google.com/)"
        expected_output = [("to Google", "https://www.google.com/")]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_multiple_links(self):
        text = "This is a text with a link [to Google](https://www.google.com/) and [to YouTube](https://www.youtube.com/)"
        expected_output = [
            ("to Google", "https://www.google.com/"),
            ("to YouTube", "https://www.youtube.com/")
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_image_and_link(self):
        text = "This is a text with ![an image of Godzilla](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg) and link [to Google](https://www.google.com/)"
        expected_images_output = [("an image of Godzilla", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg")]
        expected_link_output = [("to Google", "https://www.google.com/")]
        self.assertEqual(extract_markdown_images(text), expected_images_output)
        self.assertEqual(extract_markdown_links(text), expected_link_output)

class TestSplitNodesImagesAndLinks(unittest.TestCase):
    def test_split_one_image_one_node(self):
        text_node = TextNode(
            "this is a text and this is ![an image of Empire State Building](https://www.esbnyc.com/sites/default/files/2024-06/ESB-DarkBlueSky.jpg)", 
            TextType.TEXT)
        expected_output = [
            TextNode("this is a text and this is ", TextType.TEXT),
            TextNode(
                "an image of Empire State Building", 
                TextType.IMAGE, 
                "https://www.esbnyc.com/sites/default/files/2024-06/ESB-DarkBlueSky.jpg"
                )
        ]
        self.assertEqual(split_nodes_image([text_node]), expected_output)

    def test_split_two_images_one_node(self):
        text_node = TextNode(
            "the first image is ![a cat](https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_3x2.jpg) and the second image is ![a dog](https://cdn.britannica.com/79/232779-050-6B0411D7/German-Shepherd-dog-Alsatian.jpg)", 
            TextType.TEXT)
        expected_output = [
            TextNode("the first image is ", TextType.TEXT),
            TextNode(
                "a cat", 
                TextType.IMAGE, 
                "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_3x2.jpg"
                ),
            TextNode(" and the second image is ", TextType.TEXT),
            TextNode(
                "a dog", 
                TextType.IMAGE, 
                "https://cdn.britannica.com/79/232779-050-6B0411D7/German-Shepherd-dog-Alsatian.jpg"
                )
        ]
        self.assertEqual(split_nodes_image([text_node]), expected_output)

    def test_split_one_image_two_nodes(self):
        text_nodes = [
            TextNode(
                "this node has an image of ![a cat](https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_3x2.jpg)", 
                TextType.TEXT
                ),
            TextNode(
                "and there is ![a dog](https://cdn.britannica.com/79/232779-050-6B0411D7/German-Shepherd-dog-Alsatian.jpg) in the second node", 
                TextType.TEXT
                )
        ]
        expected_output = [
            TextNode("this node has an image of ", TextType.TEXT),
            TextNode(
                "a cat", 
                TextType.IMAGE, 
                "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_3x2.jpg"
                ),
            TextNode("and there is ", TextType.TEXT),
            TextNode(
                "a dog", 
                TextType.IMAGE, 
                "https://cdn.britannica.com/79/232779-050-6B0411D7/German-Shepherd-dog-Alsatian.jpg"
                ),
            TextNode(" in the second node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_image(text_nodes), expected_output)

    def test_split_two_images_two_nodes(self):
        text_nodes = [
            TextNode(
                "![a dog](https://i.imgur.com/OB0y6MR.jpg) and ![a cat](https://i.imgur.com/CzXTtJV.jpg)", 
                TextType.TEXT
                ),
            TextNode(
                "second node has ![a placeholder image](https://dummyimage.com/700x300.png) and ![another placeholder image](https://dummyimage.com/800x400.png) and then some text after", 
                TextType.TEXT
                )
        ]
        expected_output = [
            TextNode("a dog", TextType.IMAGE, "https://i.imgur.com/OB0y6MR.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("a cat", TextType.IMAGE, "https://i.imgur.com/CzXTtJV.jpg"),
            TextNode("second node has ", TextType.TEXT),
            TextNode("a placeholder image", TextType.IMAGE, "https://dummyimage.com/700x300.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another placeholder image", TextType.IMAGE, "https://dummyimage.com/800x400.png"),
            TextNode(" and then some text after", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_image(text_nodes), expected_output)

    def test_split_one_link_one_node(self):
        text_node = TextNode("in this node there's a link [to google](https://www.google.com/) website", TextType.TEXT)
        expected_output = [
            TextNode("in this node there's a link ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "https://www.google.com/"),
            TextNode(" website", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link([text_node]), expected_output)

    def test_split_two_links_one_node(self):
        text_node = TextNode(
            "This is a text node with a link [to Google](https://www.google.com/) and [to YouTube](https://www.youtube.com/)", 
            TextType.TEXT
            )
        expected_output = [
            TextNode("This is a text node with a link ", TextType.TEXT),
            TextNode("to Google", TextType.LINK, "https://www.google.com/"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to YouTube", TextType.LINK, "https://www.youtube.com/")
        ]
        self.assertEqual(split_nodes_link([text_node]), expected_output)

    def test_split_one_link_two_nodes(self):
        text_nodes = [
            TextNode("This text node has a link [to Google](https://www.google.com/)", TextType.TEXT),
            TextNode("[YouTube link](https://www.youtube.com/) is in the second text node", TextType.TEXT)
        ]
        expected_output = [
            TextNode("This text node has a link ", TextType.TEXT),
            TextNode("to Google", TextType.LINK, "https://www.google.com/"),
            TextNode("YouTube link", TextType.LINK, "https://www.youtube.com/"),
            TextNode(" is in the second text node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(text_nodes), expected_output)

    def test_split_two_links_two_nodes(self):
        text_nodes = [
            TextNode(
                "First node with a link [to Google](https://www.google.com/) and a link [to YouTube](https://www.youtube.com/)", 
                TextType.TEXT
                ),
            TextNode(
                "Second node has two links [to boot.dev](https://www.boot.dev)[to W3 Schools](https://www.w3schools.com)", 
                TextType.TEXT
                )
        ]
        expected_output = [
            TextNode("First node with a link ", TextType.TEXT),
            TextNode("to Google", TextType.LINK, "https://www.google.com/"),
            TextNode(" and a link ", TextType.TEXT),
            TextNode("to YouTube", TextType.LINK, "https://www.youtube.com/"),
            TextNode("Second node has two links ", TextType.TEXT),
            TextNode("to boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("to W3 Schools", TextType.LINK, "https://www.w3schools.com")
        ]
        self.assertEqual(split_nodes_link(text_nodes), expected_output)

    def test_split_one_link_one_image_one_node(self):
        text_node = TextNode(
            "this node has a link [to Google](https://www.google.com/) and an image of ![a dog](https://i.imgur.com/OB0y6MR.jpg)", 
            TextType.TEXT
            )
        expected_output = [
            TextNode("this node has a link ", TextType.TEXT),
            TextNode("to Google", TextType.LINK, "https://www.google.com/"),
            TextNode(" and an image of ", TextType.TEXT),
            TextNode("a dog", TextType.IMAGE, "https://i.imgur.com/OB0y6MR.jpg")
        ]
        self.assertEqual(split_nodes_image(split_nodes_link([text_node])), expected_output)

    def test_split_one_link_one_image_two_nodes(self):
        text_nodes = [
            TextNode(
                "First node with a link [to Google](https://www.google.com/) and an image ![of 1 pixel dot](https://dummyimage.com/1x1.png)", 
                TextType.TEXT
                ),
            TextNode(
                "Second node has an image ![of 4 pixel dot](https://dummyimage.com/2x2.png)[and a link to W3 Schools](https://www.w3schools.com)", 
                TextType.TEXT
                )
        ]
        expected_output = [
            TextNode("First node with a link ", TextType.TEXT),
            TextNode("to Google", TextType.LINK, "https://www.google.com/"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("of 1 pixel dot", TextType.IMAGE, "https://dummyimage.com/1x1.png"),
            TextNode("Second node has an image ", TextType.TEXT),
            TextNode("of 4 pixel dot", TextType.IMAGE, "https://dummyimage.com/2x2.png"),
            TextNode("and a link to W3 Schools", TextType.LINK, "https://www.w3schools.com")
        ]
        self.assertEqual(split_nodes_image(split_nodes_link(text_nodes)), expected_output)

    def test_split_varied_images_varied_links_multiple_nodes(self):
        text_nodes = [
            TextNode("The first node has ![an image of 16 pixels](https://dummyimage.com/4x4.png)", TextType.TEXT),
            TextNode("While the second node is just text", TextType.TEXT),
            TextNode("The third node has [a link to Google](https://www.google.com/)![and an image of 64 pixels](https://dummyimage.com/8x8.png)", TextType.TEXT),
            TextNode("", TextType.TEXT),
            TextNode("![100 pixels](https://dummyimage.com/10x10.png)[a link to boot.dev](https://www.boot.dev)![another image](https://www.boot.dev/img/bootdev-logo-full-small.webp)[and another link](https://bsky.app/)", TextType.TEXT)
        ]
        expected_output = [
            TextNode("The first node has ", TextType.TEXT),
            TextNode("an image of 16 pixels", TextType.IMAGE, "https://dummyimage.com/4x4.png"),
            TextNode("While the second node is just text", TextType.TEXT),
            TextNode("The third node has ", TextType.TEXT),
            TextNode("a link to Google", TextType.LINK, "https://www.google.com/"),
            TextNode("and an image of 64 pixels", TextType.IMAGE, "https://dummyimage.com/8x8.png"),
            TextNode("100 pixels", TextType.IMAGE, "https://dummyimage.com/10x10.png"),
            TextNode("a link to boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("another image", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
            TextNode("and another link", TextType.LINK, "https://bsky.app/")
        ]
        self.assertEqual(split_nodes_image(split_nodes_link(text_nodes)), expected_output)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_only(self):
        text = "This is a text value without any other syntax"
        expected_output = [TextNode("This is a text value without any other syntax", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_bold(self):
        text = "This is a **bold text** value with **more bold text**"
        expected_output = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" value with ", TextType.TEXT),
            TextNode("more bold text", TextType.BOLD)
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_italic(self):
        text = "Some *italic text* with *more italic* text"
        expected_output = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("more italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_code(self):
        text = "`Code block with some [code]` and then some text"
        expected_output = [
            TextNode("Code block with some [code]", TextType.CODE),
            TextNode(" and then some text", TextType.TEXT)
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_multiple_delimiters(self):
        text = "This text value has **some bold text** as well as *italic text* and `a code block at the end`"
        expected_output = [
            TextNode("This text value has ", TextType.TEXT),
            TextNode("some bold text", TextType.BOLD),
            TextNode(" as well as ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("a code block at the end", TextType.CODE)
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_images(self):
        text = "There's ![an image of the boot.dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) here"
        expected_output = [
            TextNode("There's ", TextType.TEXT),
            TextNode("an image of the boot.dev logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
            TextNode(" here", TextType.TEXT)
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_links(self):
        text = "The text in this variable contains [a link to boot.dev](https://www.boot.dev/)"
        expected_output = [
            TextNode("The text in this variable contains ", TextType.TEXT),
            TextNode("a link to boot.dev", TextType.LINK, "https://www.boot.dev/")
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_delimiters_and_image(self):
        text = "There's **a bold** and *italic* text here, plus ![an image](https://dummyimage.com/1x1.png)"
        expected_output = [
            TextNode("There's ", TextType.TEXT),
            TextNode("a bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text here, plus ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://dummyimage.com/1x1.png")
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_delimiters_and_link(self):
        text = "`Some code at the start` and *italic* text and then [a link](https://google.com/)"
        expected_output = [
            TextNode("Some code at the start", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and then ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://google.com/")
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_image_and_link(self):
        text = "This text value has [a link](https://google.com/) and then ![an image](https://dummyimage.com/2x2.png)"
        expected_output = [
            TextNode("This text value has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://google.com/"),
            TextNode(" and then ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://dummyimage.com/2x2.png")
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_delimiters_image_link(self):
        text = "![An image at the start](https://dummyimage.com/40x40.png) leading to **some bold text** followed by `a code block` *and in italics* before [a link at the end](https://dummyimage.com/)"
        expected_output = [
            TextNode("An image at the start", TextType.IMAGE, "https://dummyimage.com/40x40.png"),
            TextNode(" leading to ", TextType.TEXT),
            TextNode("some bold text", TextType.BOLD),
            TextNode(" followed by ", TextType.TEXT),
            TextNode("a code block", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("and in italics", TextType.ITALIC),
            TextNode(" before ", TextType.TEXT),
            TextNode("a link at the end", TextType.LINK, "https://dummyimage.com/")
            ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_delimiters_image_link_2(self):
        text = "Massive text value [with a link](https://dummyimage.com/) and ![an image](https://dummyimage.com/2x2.png)![followed by another image](https://dummyimage.com/1x1.png) with `code block` and `[more code in here]` **with bold****and more bold text** and finally *italics*"
        expected_output = [
            TextNode("Massive text value ", TextType.TEXT),
            TextNode("with a link", TextType.LINK, "https://dummyimage.com/"),
            TextNode(" and ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://dummyimage.com/2x2.png"),
            TextNode("followed by another image", TextType.IMAGE, "https://dummyimage.com/1x1.png"),
            TextNode(" with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("[more code in here]", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("with bold", TextType.BOLD),
            TextNode("and more bold text", TextType.BOLD),
            TextNode(" and finally ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

if __name__ == "__main__":
    unittest.main()