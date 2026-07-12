import av
from pptx.oxml.ns import nsdecls, qn
from pptx.slide import Slide as PptxSlide
from pptx.util import Emu

from create_slides.Movie import Movie

GAP = Emu(228600)  # 0.25 in between movies
ASPECT = 16 / 9

CLICK_PAR_TEMPLATE = """\
<p:par>
  <p:cTn id="{id0}" fill="hold">
    <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
    <p:childTnLst>
      <p:par>
        <p:cTn id="{id1}" fill="hold">
          <p:stCondLst><p:cond delay="0"/></p:stCondLst>
          <p:childTnLst>
            <p:par>
              <p:cTn id="{id2}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="clickEffect">
                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                <p:childTnLst>
                  <p:cmd type="call" cmd="playFrom(0.0)">
                    <p:cBhvr>
                      <p:cTn id="{id3}" dur="{duration_ms}" fill="hold"/>
                      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                    </p:cBhvr>
                  </p:cmd>
                </p:childTnLst>
              </p:cTn>
            </p:par>
          </p:childTnLst>
        </p:cTn>
      </p:par>
    </p:childTnLst>
  </p:cTn>
</p:par>"""

MEDIA_NODE_TEMPLATE = """\
<p:video>
  <p:cMediaNode vol="80000">
    <p:cTn id="{id0}" fill="hold" display="0">
      <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
    </p:cTn>
    <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
  </p:cMediaNode>
</p:video>"""

TIMING_TEMPLATE = """\
<p:timing {nsdecls}>
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                {click_pars}
              </p:childTnLst>
            </p:cTn>
            <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
            <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
          </p:seq>
          {media_nodes}
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>"""


def movie_duration_ms(movie: Movie) -> int:
    with av.open(str(movie.video_path)) as container:
        return int(container.duration / 1000)


def add_click_sequence_timing(
    pptx_slide: PptxSlide, movies: list[Movie], shape_ids: list[int]
) -> None:
    """One plain click per video plays it in order; the next click changes slide."""
    from pptx.oxml import parse_xml

    click_pars = []
    next_id = 3
    for movie, spid in zip(movies, shape_ids):
        click_pars.append(
            CLICK_PAR_TEMPLATE.format(
                id0=next_id,
                id1=next_id + 1,
                id2=next_id + 2,
                id3=next_id + 3,
                duration_ms=movie_duration_ms(movie),
                spid=spid,
            )
        )
        next_id += 4
    media_nodes = []
    for spid in shape_ids:
        media_nodes.append(MEDIA_NODE_TEMPLATE.format(id0=next_id, spid=spid))
        next_id += 1

    timing_xml = TIMING_TEMPLATE.format(
        nsdecls=nsdecls("p"),
        click_pars="\n".join(click_pars),
        media_nodes="\n".join(media_nodes),
    )
    slide_element = pptx_slide._element
    existing_timing = slide_element.find(qn("p:timing"))
    if existing_timing is not None:
        slide_element.remove(existing_timing)
    slide_element.append(parse_xml(timing_xml))


def add_slide_movies(
    pptx_slide: PptxSlide,
    movies: list[Movie],
    area_position: tuple[int, int],
    area_size: tuple[int, int],
) -> None:
    """Lay 16:9 videos out in one row, centered, played by successive plain clicks."""
    if not movies:
        return

    area_x, area_y = area_position
    area_w, area_h = area_size

    usable_w = area_w - GAP * (len(movies) - 1)
    movie_w = min(usable_w // len(movies), int(area_h * ASPECT))
    movie_h = int(movie_w / ASPECT)
    row_w = movie_w * len(movies) + GAP * (len(movies) - 1)
    left = area_x + (area_w - row_w) // 2
    top = area_y + (area_h - movie_h) // 2
    shape_ids = []
    for movie in movies:
        movie_shape = pptx_slide.shapes.add_movie(
            str(movie.video_path),
            Emu(left),
            Emu(top),
            Emu(movie_w),
            Emu(movie_h),
            poster_frame_image=str(movie.poster_path),
            mime_type="video/mp4",
        )
        shape_ids.append(movie_shape.shape_id)
        left += movie_w + GAP
    add_click_sequence_timing(pptx_slide, movies, shape_ids)
